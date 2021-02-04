# Imports required API libraries.
from discord import Embed
from discord.ext.commands import Cog
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash
from ..api.SlashAPI import SlashAPI as SAPI

# Imports additional libraries used.
from json import dumps

class Utils(Cog):
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

        # Check if we're searching for a specific command name.
        if name in ["", None]:
            embed = Embed.from_dict(SAPI.read("help")["embed"])
            await ctx.send(embeds = [embed])
        else:
            embed = Embed.from_dict(SAPI.read(name)["help"])
            await ctx.send(embeds = [embed])

    @cog_slash(**SAPI.read("ping")["decorator"])
    async def _ping(self, ctx: SlashContext):
        """ Returns the bot's latency as milliseconds. """

        # Get the latency from micro and bring to milli with roundup.
        latency = round(self.bot.latency * 1000)

        await ctx.send(
            content = f":ping_pong: Pong! Responded at `{latency}` ms.",
            hidden = True
        )

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """ Helps handle logic for the about menu. """

        # Ignore if it's from the bot, otherwise check it out.
        if user.id == self.bot.id:
            pass
        else:
            embeds = [
                SAPI.read("about")["embeds"][0],
                SAPI.read("about")["embeds"][1]
            ]

            for embed in embeds:
                _embed = Embed.from_dict(embed)

                if _embed in reaction.message.embeds:
                    pos = 1 if Embed.from_dict(embeds[0]) else 0
                    emote = "\N{LEFTWARDS BLACK ARROW}" if pos is 0 else "\N{BLACK RIGHTWARDS ARROW}"

                    await reaction.message.edit(embeds = [embeds[pos]])
                    await reaction.message.remove_reaction(emote, user)

    @cog_slash(**SAPI.read("about")["decorator"])
    async def _about(self, ctx: SlashContext):
        """ Provides an embed showing information about the bot. """

        embeds = [
            Embed.from_dict(SAPI.read("about")["embeds"][0]),
            Embed.from_dict(SAPI.read("about")["embeds"][1])
        ]

        for embed in embeds:
            msg = await ctx.send(embeds = [embed])

        # TODO: Uncomment once 1.0.9 releases to allow .send() returned as discord.Message object.
        # await _msg.add_reaction("\N{LEFTWARDS BLACK ARROW}")
        # await _msg.add_reaction("\N{BLACK RIGHTWARDS ARROW}")

def setup(bot):
    bot.add_cog(Utils(bot))
