__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
main.py
- creates a Flask app instance and registers the database object
"""

import os, sys
import discord
import logging
from logging.config import dictConfig
from statesman_discord.bot.client import DiscordClient
from dotenv import load_dotenv, find_dotenv


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s %(module)s, line %(lineno)d: %(message)s",
            }
        },
        "handlers": {"console": {"class": "logging.StreamHandler", "stream": "ext://sys.stdout", "formatter": "default"}},
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)

intents = discord.Intents.default()
intents.message_content = True

token = os.environ.get("DISCORD_TOKEN")
if token is None:
    logging.error("Environment variable 'DISCORD_TOKEN' is not set.")
    sys.exit(1)

client = DiscordClient(intents=intents)
client.run(token)
