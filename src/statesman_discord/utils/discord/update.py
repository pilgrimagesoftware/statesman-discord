__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
commands.py
- Discord command functions
"""


import logging, os, json
import requests
from statesman_discord.utils.discord import _get_commands_url

logging.info("Register Discord commands...")

url = _get_commands_url()
logging.debug("url: %s", url)

headers = {"Authorization": f"Bot {os.environ['DISCORD_TOKEN']}"}

commands_file = os.environ["DISCORD_COMMANDS_FILE_PATH"]
logging.info("Loading commands file '%s'...", commands_file)
with open(commands_file, "r") as f:
    commands = json.load(f)
    logging.debug("commands: %s", commands)

r = requests.post(url, headers=headers, json=commands)
logging.info("response: code=%d, headers=%s, body=%s", r.status_code, r.headers, r.json())
