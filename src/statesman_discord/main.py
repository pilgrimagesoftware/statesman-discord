__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
main.py
- creates a Flask app instance and registers the database object
"""

import os, sys
import discord
from statesman_discord.bot.client import DiscordClient


intents = discord.Intents.default()
intents.message_content = True

token = os.environment.get("DISCORD_TOKEN")
if token is None:
    sys.exit(1)

client = DiscordClient(intents=intents)
client.run(token)
