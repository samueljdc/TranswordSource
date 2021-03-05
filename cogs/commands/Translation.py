# 3rd party libraries
from discord import Embed, Member
from discord.utils import get
from discord.ext.commands import Cog
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash
from asyncio import get_event_loop
from math import floor

# Local libraries
from ..api.SlashAPI import SlashAPI as SAPI
from ..api.DeepLAPI import DeepLAPI as DAPI
from ..api import Errors

class Translation(Cog):
    """ A cog handling all translation commands for the Bot. """

    def __init__(self, bot):
        self.bot = bot

        # Define the DeepL API access.
        self.key = open(".AUTHKEY", "r").read()

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

        # Invoke a response to clean the inputs.
        await ctx.respond(eat = True)

        if formality != "":
            if target in ["EN", "EN-GB", "EN-US",
                          "ES", "JA", "ZH"]:
                await ctx.send(
                    content = f"Sorry {ctx.author.mention}, but `{target}` is not a supported language for formal formatting!\n(Formality argument has been ignored.)",
                    hidden = True
                )
            else:
                options.append(["formality", formality])
        if format != "":
            options.append(["split_sentences", format])

        # Define the rules of how our translation can begin.
        translation = {
            "chars": len(text),
            "limit": 200,
            "patron": {"isPlus": False, "isPremium": False}
        }

        # Check if the person is within their character limits.
        if translation["chars"] <= translation["limit"]:
            translation = DAPI(self.key).translate(
                text = text,
                target = target,
                types = options
            )["translations"][0]
        else:
            await ctx.send(
                content = f"Sorry {ctx.author.mention}, but your message exceeds the `{translation['limit']}` character limit with a total of `{translation['chars']}` characters!\nIn order to receive more character usage, please consider checking out our [Patreon tiers](https://www.patreon.com/transword) here.",
                hidden = True
            )
            translation = False

        try:
            if translation:
                # Set a flag table for the appropriate flags.
                flags = {
                    "DE": "flag_de",
                    "EN": "flag_us",
                    "FR": "flag_fr",
                    "IT": "flag_it",
                    "JA": "flag_jp",
                    "ES": "flag_es",
                    "NL": "flag_nl",
                    "PL": "flag_pl",
                    "PT": "flag_pt",
                    "RU": "flag_ru",
                    "ZH": "flag_cn"
                }

                # Pull the embed and make some modifications.
                embed = Embed.from_dict(SAPI.read("translate")["embed"])
                embed.set_field_at(0, name = f":{flags[translation['detected_source_language']]}: `{translation['detected_source_language']}`",   value = text,                   inline = True)
                embed.set_field_at(1, name = f":{flags[target]}: `{target}`",                                                                     value = translation["text"],    inline = True)
                embed.set_author(name = ctx.author, url = f"https://discord.com/users/{ctx.author.id}", icon_url = ctx.author.avatar_url)

                await ctx.send(embeds = [embed])
        except Errors.ScriptError as error:
            await ctx.send(content = f"Error attempting to translate: `{error}`")

    @Cog.listener()
    async def on_message(self,
                         message):
        """ Handle our automatic translations for those with the role(s). """

        # Define the rules of how our translation can begin.
        options = [["preserve_formatting", "0"]]
        translation = {
            "chars": len(message.content),
            "limit": 200,
            "patron": {"isPlus": False, "isPremium": False}
        }

        # Check for if the webhook is in the server.
        async def check(name):
            webhooks = await message.guild.webhooks()

            for hook in webhooks:
                if hook.name == name:
                    await hook.delete()
                    break

        # Check for the specific translation role.
        def retrieve():
            member = get(message.guild.members, name = message.author.name)

            for role in member.roles:
                if "auto" in role.name:
                    return get(member.roles, name = role.name)

        # Allow the bot to "imitate" the user profile.
        role = retrieve()
        exists = await check("Transword")

        if role:
            # Set up the base details.
            target = role.name.replace("auto", "")
            hook = await message.channel.create_webhook(
                name = "Transword",
                reason = "Automatic translation service."
            )

            # Make sure that the bot is not trying to loop on itself.
            if int(message.author.discriminator):
                # Check if the person is within their character limits.
                if translation["chars"] <= translation["limit"]:
                    translation = DAPI(self.key).translate(
                        text = message.content,
                        target = target,
                        types = options
                    )["translations"][0]
                else:
                    translation = False

                # Finally send it off.
                if translation:
                    # Set a flag table for the appropriate flags.
                    flags = {
                        "DE": "flag_de",
                        "EN": "flag_us",
                        "FR": "flag_fr",
                        "IT": "flag_it",
                        "JA": "flag_jp",
                        "ES": "flag_es",
                        "NL": "flag_nl",
                        "PL": "flag_pl",
                        "PT": "flag_pt",
                        "RU": "flag_ru",
                        "ZH": "flag_cn"
                    }

                    await hook.send(
                        f":{flags[translation['detected_source_language']]}: `{translation['detected_source_language']}`: {message.content}\n" +
                        f":{flags[target]}: `{target}`: {translation['text']}",
                        username = message.author.name,
                        avatar_url = message.author.avatar_url
                    )
                    await message.delete()

    @cog_slash(**SAPI.read("transauto")["decorator"])
    async def _transauto(self,
                         ctx: SlashContext,
                         target: str):
        """ Automatically translates foreign language text into another one specified. """

        # Define automatic translation role logic.
        automatic = {
            "name": f"auto{target}",
            "give": True
        }

        # Check for if the role is in the server.
        async def check(role):
            roles = await ctx.guild.fetch_roles()
            result = False
            result = True in (_role.name == role for _role in roles)

            return result

        # Check for if the user needs it given or removed.
        if await check(automatic["name"]):
            for _role in ctx.author.roles:
                if _role.name == automatic["name"]:
                    automatic["give"] = False
        else:
            await ctx.guild.create_role(name = automatic["name"])

        # Now handle the addition/removal of the role.
        automatic["role"] = get(ctx.guild.roles, name = automatic["name"])

        if automatic["give"]:
            await ctx.author.add_roles(automatic["role"])
            await ctx.send(
                content = f"Automatic translation for `{target}` is now on!\nAll future messages from you will now be deleted and translated.",
                hidden = True
            )
        else:
            await ctx.author.remove_roles(automatic["role"])
            await ctx.send(
                content = f"Automatic translation for `{target}` is now off.\nYour future messages will no longer be translated for you.",
                hidden = True
            )

    @cog_slash(**SAPI.read("stats")["decorator"])
    async def _stats(self,
                     ctx: SlashContext):
        """ Provides a list of statistics for the bot's usage. """

        # Collect information about our usages through the DeepL API.
        translation = DAPI(self.key).usage()
        progress = floor(
            (translation["character_count"] / translation["character_limit"])
            * 12
        )

        embed = Embed.from_dict(SAPI.read("stats")["embed"])
        embed.set_field_at(0, name = "Bot Usage",       value = "`" + str(translation["character_count"]) + "`",    inline = True)
        embed.set_field_at(1, name = "Bot Limit",       value = "`" + str(translation["character_limit"]) + "`",    inline = True)
        embed.set_field_at(2, name = "Progress Bar",    value = "`[" +
            "".join("=" for _n in range(progress)) +
            "".join(" " for _n in range(12 - progress))
        + "]`",                                                                                                     inline = True)
        embed.set_field_at(3, name = "Character Usage", value = "`TBA.`",                                           inline = True)
        embed.set_field_at(4, name = "Character Limit", value = "`200`",                                            inline = True)
        embed.set_author(name = ctx.author, url = f"https://discord.com/users/{ctx.author.id}", icon_url = ctx.author.avatar_url)

        # Invoke a response to clean the inputs.
        await ctx.respond()
        await ctx.send(embeds = [embed])

def setup(bot):
    bot.add_cog(Translation(bot))
