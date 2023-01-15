__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
- Discord utilities
"""


from statesman_discord import constants
import os, logging


_discord_base = "https://discord.com/api/v10"

def _get_commands_url():
    logging.debug("")
    url = os.environ.get(constants.DISCORD_API_URL, f"{_discord_base}/applications/{os.environ[constants.DISCORD_CLIENT_ID]}/commands")
    logging.debug("url: %s", url)
    return url

def _get_interaction_response_url(token:str):
    logging.debug("")
    url = os.environ.get(constants.DISCORD_API_URL, f"{_discord_base}/webhooks/{os.environ[constants.DISCORD_CLIENT_ID]}/{token}/messages/@original")
    logging.debug("url: %s", url)
    return url
