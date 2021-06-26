# Normal libraries
import logging

# 3rd-party libraries
from discord import Embed
from discord.ext.commands import Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_slash
from discord_slash.model import SlashCommandOptionType as opt_type
from ..model import BaseCommand
from ..deepl import DeepL
from ..feeder import Feeder
from ..errors import TranslateError, HttpError

logging.getLogger("Errors")

base: BaseCommand = BaseCommand(
    name="trl",
    description="Translates text from one language to another.",
    guild_ids=[799685484313968670],
    options=[
        dict(
            name="target",
            description="The language to translate into.",
            type=opt_type.STRING,
            required=True,
            choices=[dict(name=name, value=name) for name in DeepL(auth="").target_lang[:24]]
        ),
        dict(name="text", description="The text to translate.", type=opt_type.STRING, required=True),
        dict(
            name="formality",
            description="How formal/informal the translation is.",
            type=opt_type.STRING,
            required=False,
            choices=[
                dict(name="Formal", value="more"),
                dict(name="Informal", value="less")
            ]
        ),
        dict(name="format", description="How the translation will be printed.", type=opt_type.STRING, required=False)
    ]
)

class Translate(Cog):
    """
    A translation command for the bot.
    Relies off of the BaseCommand class for construction.
    """
    def __init__(self,
                 bot) -> None:
        self.bot = bot

    @cog_slash(**base.model)
    async def command(self,
                      ctx: SlashContext,
                      target: str,
                      text: str,
                      formality: str="less",
                      format: str="1") -> None:
        _target: str = target
        _formality: str = formality
        _format: str = format
        key: str = Feeder().read_token(key="deepl_key")
        api: DeepL = DeepL(auth=key)

        print(api._auth)

        await ctx.defer()

        try:
            try:
                if api.is_valid():
                    print("we got in")
                    limits: list = {"chars": 350}
                    if _formality == "more":
                        if _target in api.formal_exceptions:
                            _formality = "less"
                            await ctx.send(
                                content=f"Sorry, but the {target} language is not a supported language for formal writing!\n(Automatically registered as informal instead.)",
                                hidden=True
                            )
                    if len(text) <= limits["chars"]:
                        translation = api.translate(
                            text=text,
                            target=_target,
                            formality=_formality,
                            preserve_formatting=_format
                        )["translations"][0]

                        if translation:
                            embed: Embed = Embed(title="Translation", color=0x5865F2)
                            embed.add_field(
                                name="Source",
                                value=text
                            )
                            embed.add_field(
                                name="Result",
                                value=translation["text"]
                            )
                            embed.set_author(
                                name=ctx.author,
                                icon_url=ctx.author.avatar_url,
                                url=f"https://discord.com/users/{ctx.author.id}"
                            )
                            await ctx.send(embeds=[embed])
                    else:
                        await ctx.send(
                            content=f"Sorry, but your translation request exceeds our `{limits['chars']}` character limit!\n(You are currently at `len(text)`.)",
                            hidden=True
                        )
            except HttpError as error:
                logging.error(error)
                await ctx.send(
                    content=f"An error was found trying to complete the translation:\n```{error}```",
                    hidden=True
                )
        except TranslateError as error:
            logging.error(error)
            await ctx.send(
                content=f"An error was found trying to complete the translation:\n```{error}```",
                hidden=True
            )

def setup(bot):
    bot.add_cog(Translate(bot))
