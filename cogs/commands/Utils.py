# Imports required API libraries.
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash
from discord_slash.utils.manage_commands import create_option
from ..api.SlashAPI import SlashAPI as API, SlashError as Error
# from ..api.SlashAPI import SlashError as Error

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

        self.create_commands()

    def create_commands(self):
        """ Creates new commands that will be used for this cog. """

        pass

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    # TODO: Deprecate testing source once this cog is complete.
    # @cog_slash(**API.read("test"))
    # async def _test(self, ctx: SlashContext, paramone: str, paramtwo: str):
    #     """ Just a testing command. """
    #
    #     await ctx.send(
    #         content = f"Parameter one: {paramone}\nParameter two: {paramtwo}",
    #         send_type = 3
    #     )

    @cog_slash(**API.read("help")["decorator"])
    async def _help(self, ctx: SlashContext, name: str = None):
        """ Returns an embed showing the bot's commands. """

        # Check if the name field is empty or not.
        try:
            if name in ["", None]:
                embed = discord.Embed.from_dict(API.read("help")["embed"])
                await ctx.send(embeds = [embed])
            else:
                await ctx.send(content = "Sorry, but we can't support searching specific command names yet!")
        except Error:
            # Return the error if it fails.
            exception = API.parse_error(400)
            print(f"[UTILS] {exception}")

def setup(bot):
    bot.add_cog(Utils(bot))
