__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
setup.py
- Discord setup
"""

from flask import current_app
import os, json
from statesman_discord import constants
from statesman_discord.utils.discord.commands import register_command


def register_commands():
    current_app.logger.debug("")

    with open(os.environ[constants.DISCORD_COMMANDS_FILE_PATH], "r") as f:
        commands = json.load(f)
        for command in commands:
            current_app.logger.info("Registering command: %s", command)
            register_command(command, os.environ[constants.DISCORD_CLIENT_SECRET])
