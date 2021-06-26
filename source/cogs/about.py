# Normal libraries
import logging

# 3rd-party libraries
from discord import Embed
from discord.ext.commands import Cog
from discord_slash import SlashContext, ComponentContext
from discord_slash.cog_ext import cog_slash
from discord_slash.utils import manage_components as button
from discord_slash.model import SlashCommandOptionType as opt_type, ButtonStyle as button_color
from ..model import BaseCommand

logging.getLogger("Errors")

base: BaseCommand = BaseCommand(
    name="about",
    description="Information about the bot.",
    guild_ids=[799685484313968670]
)

class About(Cog):
    """
    An about command for the bot.
    Relies off of the BaseCommand class for construction.
    """
    def __init__(self,
                 bot) -> None:
        self.bot = bot

    def page(self,
             position: int=1) -> Embed:
        """
        Returns the position of the embed page.

        :param position: The embed position
        :type position: int

        :return: Embed
        """
        struct: Embed = Embed(title="About", colour=0x5865F2)
        _position: int = position
        if _position == 1:
            struct.add_field(
                name="What is Transword?",
                value="Transword is the future of Discord translation bots. The purpose of Transword is to help serve as a bridge connecting communities together bound by language barriers. Whether this may be your friends, a community, or international support server, Transword aims to provide the help that you need with the best Deep Learning AI able to be offered at this time.",
                inline=False
            )
            struct.add_field(
                name="How does Transword work?",
                value="Transword utilizes the DeepL API, one of the best APIs that are out there to be offered to the public for foreign language translation. This API has been specifically chosen for its accuracy and authenticity over the amount of languages that it can translate. Rest assured, Transword will never be perfect, but it is far better than Google Translate and Yandex, despite having less languages to choose from.",
                inline=False
            )
            struct.add_field(
                name="Is this for free?",
                value="Yes! Transword will *always* stay free for the public to use. However, if you would like to help support the project, then please consider joining our Support Server for future cases where the possibility may open up to offer upgrades.",
                inline=False
            )
        elif _position == 2:
            struct.add_field(
                name="Why do you limit to 200 characters?",
                value="Unfortunately, not everything comes for free in the real world. Here on Discord, we wish to provide our users the most lenient options available for their own personal use. Transword has been no exception to this, and we give 200 characters available for translation. Statistically, most internet viewers type on average 180 characters per message. *20 extra for you to use the emotes!*",
                inline=False
            )
            struct.add_field(
                name="Where can I contact for support?",
                value="Please reach out to us on our [Discord Server here](https://discord.gg/4n7WRHp86P) if you have any questions, concerns, problems or feedback. Your voice is important to us in order to provide a more qualitative experience for everyone!",
                inline=False
            )
            struct.add_field(
                name="Do you have more information about this bot elsewhere?",
                value="Of course! If you would like to see what this bot is all about in further detail, then please check out our [official website](https://transword.xyz) link here. All feedback is generously appreciated.",
                inline=False
            )

        struct.set_thumbnail(url=self.bot.user.avatar_url)
        struct.set_footer(text=f"This bot was made by fl0w#0001. | Page {_position}/2")
        return struct

    async def button_logic(self,
                           *args) -> None:
        """
        Defines the logic for how button interactions are handled.

        :param args: Multiple handled arguments.
        :type args: mixed

        :return: None
        """
        try:
            btn_ctx: ComponentContext = await button.wait_for_component(
                client=self.bot,
                components=args[0]
            )
        except:
            pass
        else:
            if btn_ctx.custom_id == "1":
                await btn_ctx.edit_origin(embeds=[self.page()])
            elif btn_ctx.custom_id == "2":
                await btn_ctx.edit_origin(embeds=[self.page(2)])

    @cog_slash(**base.model)
    async def command(self,
                      ctx: SlashContext) -> None:
        buttons: list = [
            button.create_button(custom_id="1", style=button_color.blue, label="1"),
            button.create_button(custom_id="2", style=button_color.blue, label="2")
        ]
        action_row = button.create_actionrow(*buttons)
        msg = await ctx.send(embeds=[self.page()], components=[action_row])

        while True:
            await self.button_logic(action_row)

def setup(bot):
    bot.add_cog(About(bot))
