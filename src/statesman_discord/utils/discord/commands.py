__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
commands.py
- Discord command functions
"""


from flask import current_app
import requests
from statesman_discord.utils.discord import _get_url


def register_command(command: object, token: str):
    current_app.logger.debug("")

    url = _get_url()
    current_app.logger.debug("url: %s", url)

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.post(url, headers=headers, json=command)
    current_app.logger.info("r: %s", r)
