# Imports required API libraries.
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash
from ..api.SlashAPI import SlashAPI as SAPI

# Imports additional libraries used.
from json import dumps

class Utils(commands.Cog):
    """ A cog handling all utility commands for the Bot. """

    def __init__(self, bot):
        # Makes slash commands existent if not set.
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(
                bot,
                override_type = True,
                auto_register = True,
                auto_delete = True
            )

        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_slash(**SAPI.read("help")["decorator"])
    async def _help(self, ctx: SlashContext, name: str = None):
        """ Returns an embed showing the bot's commands. """

        # Check if the name field is empty or not.
        if name in ["", None]:
            embed = discord.Embed.from_dict(SAPI.read("help")["embed"])
            await ctx.send(embeds = [embed])
        else:
            await ctx.send(content = "Sorry, but we can't support searching specific command names yet!")

    @cog_slash(**SAPI.read("ping")["decorator"])
    async def _ping(self, ctx: SlashContext):
        """ Returns the bot's latency as milliseconds. """

        # Collect the latency in microseconds, then bring to ms and round up.
        latency = round(self.bot.latency * 1000)

        await ctx.send(
            content = f":ping_pong: Pong! Responded at `{latency}` ms.",
            hidden = True
        )

    @cog_slash(**SAPI.read("about")["decorator"])
    async def _about(self, ctx: SlashContext):
        """ Provides an embed showing information about the bot. """

        embed = discord.Embed.from_dict(SAPI.read("about")["embed"])
        await ctx.send(embeds = [embed])

def setup(bot):
    bot.add_cog(Utils(bot))
