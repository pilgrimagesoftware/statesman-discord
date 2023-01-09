__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
commands.py
- Discord command functions
"""


import logging
import requests
from statesman_discord.utils.discord import _get_commands_url


def register_command(command: object, token: str):
    logging.debug("")

    url = _get_commands_url()
    logging.debug("url: %s", url)

    headers = {"Authorization": f"Bot {token}"}

    r = requests.post(url, headers=headers, json=command)
    logging.info("response: code=%d, headers=%s, body=%s", r.status_code, r.headers, r.json())


def construct_command(msg: dict) -> str:
    logging.debug("msg: %s", msg)

    cmd = msg["data"]["name"]
    logging.debug("cmd: %s", cmd)
    # TODO: check cmd

    parts = list(map(lambda x: x["name"], msg["data"]["options"]))
    logging.debug("parts: %s", parts)
    command = " ".join(parts)
    logging.debug("command: %s", command)

    return command
