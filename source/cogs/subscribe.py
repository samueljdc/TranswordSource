# Normal libraries
import logging

# 3rd-party libraries
from discord import TextChannel
from discord.utils import get
from discord.ext.commands import Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_slash
from discord_slash.model import SlashCommandOptionType as opt_type
from ..model import BaseCommand

logging.getLogger("Errors")

base: BaseCommand = BaseCommand(
    name="subscribe",
    description="Subscribes the bot to future announcements.",
    guild_ids=[799685484313968670],
    options=[
        dict(name="channel", description="The channel to subscribe under.", type=opt_type.CHANNEL, required=True)
    ]
)

class Subscribe(Cog):
    """
    A subscribe command for the bot.
    Relies off of the BaseCommand class for construction.
    """
    def __init__(self,
                 bot) -> None:
        self.bot = bot

    @cog_slash(**base.model)
    async def command(self,
                      ctx: SlashContext,
                      channel: TextChannel) -> None:
        source = get(self.bot.guilds, id=799685484313968670).get_channel(799687367400357899)
        await source.follow(destination=channel)
        await ctx.send(content="Channel has now been subscribed to for updates.", hidden=True)

def setup(bot):
    bot.add_cog(Subscribe(bot))
