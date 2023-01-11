__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
interact
- Interaction controller
"""

import pika
import os, logging, time, json
from statesman_discord import constants
from threading import Thread
from statesman_discord.utils.discord.commands import construct_command
from statesman_discord.utils.discord.messages import handle_interaction_response


def send_amqp_message(msg: dict):
    """_summary_

    Args:
        msg (_type_): _description_
    """
    logging.debug("msg: %s", msg)

    command = construct_command(msg)
    logging.debug("command: %s", command)

    body_data = {
        "sender": os.environ[constants.POD],
        "timestamp": time.time(),
        "response_data": {
            "queue": os.environ[constants.RABBITMQ_QUEUE],
            "application_id": msg["application_id"],
            "token": msg["token"],
            "raw_data": msg["data"],
        },
        "user": {
            "service": "discord",
            "org_id": msg["guild_id"],
            "canonical_id": f"discord|{msg['member']['user']['id']}",
            "data": msg["member"]["user"],
        },
        "data": {"command": command},
    }
    body = json.dumps(body_data)
    logging.debug("body: %s", body)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            os.environ[constants.RABBITMQ_HOST],
            os.environ[constants.RABBITMQ_PORT],
            os.environ[constants.RABBITMQ_VHOST],
            pika.PlainCredentials(os.environ[constants.RABBITMQ_USER], os.environ[constants.RABBITMQ_PASSWORD]),
        )
    )
    channel = connection.channel()
    try:
        channel.basic_publish(exchange=os.environ[constants.RABBITMQ_EXCHANGE], routing_key=os.environ[constants.RABBITMQ_API_QUEUE], body=body)
    except Exception as e:
        logging.exception("Exception while attempting to publish message:", e)
    finally:
        channel.close()


class MessageConsumer(Thread):
    """_summary_

    Args:
        Thread (_type_): _description_
    """

    def message_callback(self, ch, method, properties, body):
        """_summary_

        Args:
            ch (_type_): _description_
            method (_type_): _description_
            properties (_type_): _description_
            body (_type_): _description_
        """
        logging.info("ch: %s, method: %s, properties: %s, body: %s", ch, method, properties, body)

        msg = json.loads(body)
        logging.debug("msg: %s", msg)

        # TODO: check response type, handle appropriately

        handle_interaction_response(msg)

    def run(self):
        logging.info("Consumer thread started.")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                os.environ[constants.RABBITMQ_HOST],
                os.environ[constants.RABBITMQ_PORT],
                os.environ[constants.RABBITMQ_VHOST],
                pika.PlainCredentials(os.environ[constants.RABBITMQ_USER], os.environ[constants.RABBITMQ_PASSWORD]),
            )
        )
        channel = connection.channel()
        channel.basic_consume(queue=os.environ[constants.RABBITMQ_QUEUE], on_message_callback=self.message_callback, auto_ack=True)
        channel.start_consuming()
        channel.close()


consumer_thread = MessageConsumer()
consumer_thread.setDaemon(True)
consumer_thread.start()
