__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Discord utilities
"""


from flask import current_app
from statesman_discord import constants
import os


def _get_url():
    current_app.logger.debug("")
    url = os.environ.get(constants.DISCORD_API_URL, f"https://discord.com/api/v10/applications/{os.environ[constants.DISCORD_CLIENT_ID]}/commands")
    current_app.logger.debug("url: %s", url)
    return url
