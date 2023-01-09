__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
interact
- Interaction controller
"""

import pika
import os, logging, time, json
from statesman_discord import constants


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        os.environ[constants.RABBITMQ_HOST],
        os.environ[constants.RABBITMQ_PORT],
        os.environ[constants.RABBITMQ_VHOST],
        pika.PlainCredentials(os.environ[constants.RABBITMQ_USER], os.environ[constants.RABBITMQ_PASSWORD]),
    )
)

channel = connection.channel()


def send_amqp_message(msg: object):
    """_summary_

    Args:
        msg (_type_): _description_
    """

    body_data = {"sender": os.environ[constants.POD], "timestamp": time.time(), "response_queue": os.environ[constants.RABBITMQ_QUEUE], "data": msg}
    body = json.dumps(body_data)
    channel.basic_publish(exchange=os.environ[constants.RABBITMQ_EXCHANGE], routing_key=os.environ[constants.RABBITMQ_API_QUEUE], body=body)

    connection.close()


def message_callback(ch, method, properties, body):
    """_summary_

    Args:
        ch (_type_): _description_
        method (_type_): _description_
        properties (_type_): _description_
        body (_type_): _description_
    """
    logging.info("ch: %s, method: %s, properties: %s, body: %s", ch, method, properties, body)


channel.basic_consume(queue=os.environ[constants.RABBITMQ_QUEUE], on_message_callback=message_callback, auto_ack=True)
channel.start_consuming()
