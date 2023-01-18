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


creds = pika.PlainCredentials(username=os.environ[constants.RABBITMQ_USER], password=os.environ[constants.RABBITMQ_PASSWORD])
params = pika.ConnectionParameters(
    host=os.environ[constants.RABBITMQ_HOST],
    port=os.environ[constants.RABBITMQ_PORT],
    virtual_host=os.environ[constants.RABBITMQ_VHOST],
    credentials=creds,
    heartbeat=int(os.environ.get(constants.RABBITMQ_HEARTBEAT, "600")),
    blocked_connection_timeout=int(os.environ.get(constants.RABBITMQ_TIMEOUT, "300")),
)
