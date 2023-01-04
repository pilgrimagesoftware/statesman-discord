__author__ = "Paul Schifferer <paul@schifferers.net>"
"""
bot/
-
"""

import discord
from discord.ext import commands
import logging


intents = discord.Intents.default()
intents.message_content = True
intents.typing = False
intents.presences = False
intents.members = False


bot = commands.Bot(command_prefix=commands.when_mentioned, description="TBD", intents=intents)
# logger = logging.getLogger("root")


@bot.event
async def on_ready():
    logging.info("Logged on as %s (%s).", bot.user, bot.user.id)


#     async def on_message(self, message):
#         if message.author == self.user:
#             logging.debug("Ignoring message from ourselves.")
#             return

#         print(f"Message from {message.author}: {message.content}")


@bot.command()
async def add(ctx, param: int):
    """xxx

    Args:
        ctx (_type_): _description_
        param (int): _description_
    """
    logging.info("add: %d", param)
    await ctx.send(param)


# bot = DiscordBot(command_prefix="#", intents=intents)
