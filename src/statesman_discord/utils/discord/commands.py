__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
commands.py
- Discord command functions
"""


import logging
import requests
from statesman_discord.utils.discord import _get_url


def register_command(command: object, token: str):
    logging.debug("")

    url = _get_url()
    logging.debug("url: %s", url)

    headers = {"Authorization": f"Bot {token}"}

    r = requests.post(url, headers=headers, json=command)
    logging.info("r: %s", r)
