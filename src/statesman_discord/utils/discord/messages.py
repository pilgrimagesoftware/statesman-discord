__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
messages.py
- Discord messaging functions
"""


from flask import current_app
import json, logging
import requests
from statesman_discord import constants
from statesman_discord.common.exceptions import SignatureException


def send_message(response_url: str, blocks: list, private: bool):
    logging.debug("response_url: %s, blocks: %s, private: %s", response_url, blocks, private)

    response_type = "in_channel" if not private else "ephemeral"

    body = json.dumps(
        {
            "response_type": response_type,
            "blocks": blocks,
        }
    )
    logging.debug("body: %s", body)
    r = requests.post(
        response_url,
        headers={
            "Content-type": "application/json",
        },
        data=body,
    )
    logging.debug("r: %s", r)
