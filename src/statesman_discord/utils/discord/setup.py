__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
setup.py
- Discord setup
"""

import os, json, logging
from statesman_discord import constants
from statesman_discord.utils.discord.commands import register_command


def register_commands():
    logging.debug("")

    with open(os.environ[constants.DISCORD_COMMANDS_FILE_PATH], "r") as f:
        commands = json.load(f)
        for command in commands:
            logging.info("Registering command: %s", command)
            register_command(command, os.environ[constants.DISCORD_CLIENT_SECRET])
