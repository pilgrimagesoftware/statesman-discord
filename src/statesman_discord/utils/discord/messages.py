__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
messages.py
- Discord messaging functions
"""


from flask import current_app
import json, logging, os
import requests
from statesman_discord import constants
from statesman_discord.common.exceptions import SignatureException
from statesman_discord.utils.discord import _get_interaction_response_url


def send_message(response_url: str, data: list, private: bool):
    logging.debug("response_url: %s, data: %s, private: %s", response_url, data, private)

    body = json.dumps(
        {
            "private": private,
            "data": data,
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


def handle_interaction_response(msg: dict):
    logging.debug("msg: %s", msg)

    answer = msg.get("answer")
    flags = 0
    if answer is None:
        content = "TBD"
    else:
        content = "\n".join(map(lambda m: m.get("text", ""), answer.get("data", [])))
        if answer.get("private"):
            flags |= constants.MSG_FLAG_EPHEMERAL

    headers = {"Authorization": f"Bot {os.environ['DISCORD_TOKEN']}"}
    body = {
        "flags": flags,
        "content": content,
    }

    url = _get_interaction_response_url(msg["response_data"]["token"])
    r = requests.patch(url, headers=headers, json=body)
    logging.info("response: code=%d, headers=%s, body=%s", r.status_code, r.headers, r.json())
