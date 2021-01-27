# Imports required API libraries.
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash
from ..api.SlashAPI import SlashAPI as SAPI
from ..api.DeepLAPI import DeepLAPI as DAPI

# Imports additional libraries used.
from asyncio import get_event_loop

class Translation(commands.Cog):
    """ A cog handling all translation commands for the Bot. """

    def __init__(self, bot):
        # Makes slash commands existent if not set.
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(
                bot,
                override_type = True,
                auto_register = True,
                auto_delete = True
            )

        # Define the DeepL API access.
        self.key = open(".AUTHKEY", "r").read()
        self.API = DAPI(self.key)

        self.bot = bot
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    # TODO: Figure out a more organized approach for the asyncio method to run DeepL API functions.
    @cog_slash(**SAPI.read("translate")["decorator"])
    async def _translate(self,
                         ctx: SlashContext,
                         target: str,
                         text: str,
                         format: str = "",
                         formality: str = ""):
        """ Translates text from a foreign language into another one specified. """

        # CHeck if any optional arguments were passed.
        options = [["preserve_formatting", "1"]]

        if formality != "":
            options.append(["formality", formality])
        if format != "":
            options.append(["split_sentences", format])

        # Run the DeepL API to translate for us.
        information = self.API.translate(
            text = text,
            target = target,
            types = options
        )["translations"][0]

        # Pull the embed and make some modifications.
        embed = discord.Embed.from_dict(SAPI.read("translate")["embed"])
        embed.set_field_at(0,
            name = f"`{information['detected_source_language']}`",
            value = text,
            inline = True
        )
        embed.set_field_at(1,
            name = f"`{target}`",
            value = information["text"],
            inline = True
        )
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(3, embeds = [embed])

def setup(bot):
    bot.add_cog(Translation(bot))
