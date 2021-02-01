# 3rd party libraries
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash
from asyncio import get_event_loop

# Local libraries
from ..api.SlashAPI import SlashAPI as SAPI
from ..api.DeepLAPI import DeepLAPI as DAPI

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
                         formality: str = "",
                         format: str = ""):
        """ Translates text from a foreign language into another one specified. """

        # Check if any optional arguments were passed.
        options = [["preserve_formatting", "0"]]

        if formality != "":
            if target in ["EN", "EN-GB", "EN-US",
                          "ES", "JA", "ZH"]:
                await ctx.send(content = f"Sorry {ctx.author.mention}, but `{target}` is not a supported language for formal formatting!\n(Formality argument has been ignored.)")
            else:
                options.append(["formality", formality])
        if format != "":
            options.append(["split_sentences", format])

        # Run the DeepL API to translate for us as long as within character limits.
        translation = None
        
        if len(text) <= 200:
            translation = self.API.translate(
                text = text,
                target = target,
                types = options
            )["translations"][0]
        else:
            await ctx.send(content = "Sorry, but your message exceeds the `200` character limit with a total of `{chars}` characters!\nIn order to receive more character usage, please consider checking out our [Patreon tiers](https://www.patreon.com/transword) here.")
            translation = False

        if translation:
            # Pull the embed and make some modifications.
            embed = discord.Embed.from_dict(SAPI.read("translate")["embeds"][0])
            embed.set_field_at(0, name = f"`{translation['detected_source_language']}`",    value = text,                   inline = True)
            embed.set_field_at(1, name = f"`{target}`",                                     value = translation["text"],    inline = True)
            embed.set_thumbnail(url = ctx.author.avatar_url)

            await ctx.send(3, embeds = [embed])

    @cog_slash(**SAPI.read("transauto")["decorator"])
    async def _transauto(self,
                         ctx: SlashContext,
                         target: str):
        """ Automatically translates foreign language text into another one specified. """

        pass

def setup(bot):
    bot.add_cog(Translation(bot))
