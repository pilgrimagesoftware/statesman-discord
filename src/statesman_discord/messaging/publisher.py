__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
interact
- Interaction controller
"""

import pika
import os, logging, time, json, socket
from statesman_discord import constants
from threading import Thread
from statesman_discord.utils.discord.commands import construct_command
from statesman_discord.utils.discord.messages import handle_interaction_response
from statesman_discord.messaging import params


def send_amqp_message(msg: dict):
    """_summary_

    Args:
        msg (_type_): _description_
    """
    logging.debug("msg: %s", msg)

    command = construct_command(msg)
    logging.debug("command: %s", command)

    body_data = {
        "sender": os.environ.get(constants.POD, socket.gethostname()),
        "timestamp": time.time(),
        "response_data": {
            "queue": os.environ[constants.RABBITMQ_QUEUE],
            "application_id": msg["application_id"],
            "token": msg["token"],
            "raw_data": msg["data"],
        },
        "user": {
            "service": "discord",
            "org_id": f"discord|{msg['guild_id']}",
            "canonical_id": f"discord|{msg['member']['user']['id']}",
            "data": msg["member"]["user"],
        },
        "data": {"command": command},
    }
    body = json.dumps(body_data)
    logging.debug("body: %s", body)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.confirm_delivery()
    try:
        channel.basic_publish(exchange=os.environ[constants.RABBITMQ_EXCHANGE], routing_key=os.environ[constants.RABBITMQ_API_QUEUE], body=body)
    except Exception as e:
        logging.exception("Exception while attempting to publish message:", e)
    finally:
        channel.stop_consuming()
        channel.close()
        connection.close()
