# Normal libraries
import asyncio, logging
from datetime import datetime
from os import listdir, system
from os.path import isfile, join

# 3rd-party libraries
import discord, discord_slash
from discord import Intents, Status, Activity, ActivityType
from discord.ext.commands import AutoShardedBot
from discord_slash import SlashCommand
from .feeder import Feeder

class BotStruct:
    """Structure for the bot."""
    def __init__(self):
        self.prefix: str = "/"
        self.intents: Intents = Intents.all()
        self.commands: list = [
            "test",
            "about",
            "subscribe",
            "trl"
        ]
        self.bot: AutoShardedBot = AutoShardedBot(
            command_prefix=self.prefix,
            intents=self.intents,
            help_command=None
        )
        self.slash: SlashCommand = SlashCommand(
            self.bot,
            sync_commands=True,
            override_type=True
        )

        def load_cogs():
            for cmd in self.commands:
                self.bot.load_extension(f"source.cogs.{cmd}")

        load_cogs()
        self.bot.load_extension("source.errors")

struct = BotStruct()
logging.basicConfig(filename="data/logs/Bot.log", level=logging.INFO)

@struct.bot.event
async def on_ready():
    system("Transword - Terminal")
    output = "\n".join([
        f"Logged under                  : {struct.bot.user.name}#{struct.bot.user.discriminator}",
        f"User ID                       : {struct.bot.user.id}",
        f"Guilds                        : {len(struct.bot.guilds)}",
        f"Users                         : {sum(len(guild.members) for guild in struct.bot.guilds)}",
        f"Commands                      : {len(struct.slash.commands)}",
        f"discord.py Version            : {discord.__version__}",
        f"discord-interactions Version  : {discord_slash.__version__}"
    ])
    logging.info(output)
    print(output)

    await struct.bot.change_presence(
        status=Status.idle,
        activity=Activity(
            type=ActivityType.watching,
            name="you. 👀"
        )
    )

def run():
    """Runs the bot from discord.Client"""
    struct.bot.run(Feeder().read_token(key="bot_token"), bot=True)
