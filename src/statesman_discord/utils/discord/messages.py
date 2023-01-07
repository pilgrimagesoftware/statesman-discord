__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
messages.py
- Discord messaging functions
"""


from flask import current_app
import json
import requests
from statesman_discord import constants
from statesman_discord.common.exceptions import SignatureException


def send_message(response_url: str, blocks: list, private: bool):
    current_app.logger.debug("response_url: %s, blocks: %s, private: %s", response_url, blocks, private)

    response_type = "in_channel" if not private else "ephemeral"

    body = json.dumps(
        {
            "response_type": response_type,
            "blocks": blocks,
        }
    )
    current_app.logger.debug("body: %s", body)
    r = requests.post(
        response_url,
        headers={
            "Content-type": "application/json",
        },
        data=body,
    )
    current_app.logger.debug("r: %s", r)
