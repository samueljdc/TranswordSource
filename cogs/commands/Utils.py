# Sets up our discord.py libraries needed
import discord
from discord.ext import commands

# Imports additional libraries required.
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_commands import create_option
from ..api.SlashAPI import SlashAPI as API

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

    @cog_slash(**API.read(None, "test"))
    async def _test(self, ctx: SlashContext, paramone: str, paramtwo: str):
        """ Just a testing command. """

        await ctx.send(
            content = f"Parameter one: {paramone}\nParameter two: {paramtwo}",
            send_type = 3
        )

def setup(bot):
    bot.add_cog(Utils(bot))
