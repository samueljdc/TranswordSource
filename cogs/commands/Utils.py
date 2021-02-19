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
        self.bot = bot

    @cog_slash(**SAPI.read("help")["decorator"])
    async def _help(self, ctx: SlashContext, name: str = None):
        """ Returns an embed showing the bot's commands. """

        # Invoke a response to clean the inputs.
        await ctx.respond(eat = True)

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

        # Invoke a response to clean the inputs.
        await ctx.respond(eat = True)
        await ctx.send(
            content = f":ping_pong: Pong! Responded at `{latency}` ms.",
            hidden = True
        )

    # @Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     """ Helps handle logic for the about menu. """
    #
    #     # Ignore if it's from the bot, otherwise check it out.
    #     if user.id == 799697654279307314:
    #         pass
    #     else:
    #         embeds = [
    #             Embed.from_dict(SAPI.read("about")["embeds"][0]),
    #             Embed.from_dict(SAPI.read("about")["embeds"][1])
    #         ]
    #
    #         if reaction.message.embeds[0].title == "About":
    #             pos = 0 if reaction.message.embeds[0] == embeds[0] else 1
    #             emote = "\N{LEFTWARDS BLACK ARROW}" if pos == 0 else "\N{BLACK RIGHTWARDS ARROW}"
    #
    #             print(f"[REACTION_LOGIC] Determined existent! Pos: {pos}\nEmote type: {emote}")
    #
    #             await reaction.message.edit(embed = [embeds[pos]])
    #             await reaction.message.remove_reaction(emote, user)

    @cog_slash(**SAPI.read("about")["decorator"])
    async def _about(self, ctx: SlashContext):
        """ Provides an embed showing information about the bot. """

        embeds = [
            Embed.from_dict(SAPI.read("about")["embeds"][0]),
            Embed.from_dict(SAPI.read("about")["embeds"][1])
        ]

        # Invoke a response to clean the inputs.
        await ctx.respond(eat = True)

        for embed in embeds:
            msg = await ctx.send(embeds = [embed])

        # await msg.add_reaction("\N{LEFTWARDS BLACK ARROW}")
        # await msg.add_reaction("\N{BLACK RIGHTWARDS ARROW}")

    @cog_slash(**SAPI.read("vote")["decorator"])
    async def _vote(self, ctx: SlashContext):
        """ Provides a website link to vote for Transword's reputability. """

        # Set up the link for the bot voting page.
        link = "https://top.gg/bot/799697654279307314/vote"

        # Invoke a response to clean the inputs.
        await ctx.respond(eat = True)
        await ctx.send(
            content = f"If you would like to help us give more attention to this bot through the method of advertising, please consider voting for our bot in the link below! Your vote is generously appreciated to help us create a future here for Discord.\n\n{link}",
            hidden = True
        )

def setup(bot):
    bot.add_cog(Utils(bot))
