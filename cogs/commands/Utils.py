# Imports required API libraries.
from discord import Embed
from discord.ext.commands import Cog
from discord_slash import SlashCommand, SlashContext
from discord_slash.cog_ext import cog_slash
from ..api.SlashAPI import SlashAPI as SAPI

# Imports additional libraries used.
from json import dumps
from asyncio import TimeoutError

class Utils(Cog):
    """ A cog handling all utility commands for the Bot. """

    def __init__(self, bot):
        self.bot = bot

    @cog_slash(**SAPI.read("help")["decorator"])
    async def _help(self, ctx: SlashContext, name: str = None):
        """ Returns an embed showing the bot's commands. """

        # Invoke a response to clean the inputs.
        await ctx.respond()

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

    @cog_slash(**SAPI.read("about")["decorator"])
    async def _about(self, ctx: SlashContext):
        """ Provides an embed showing information about the bot. """

        # Set up the structure of the command.
        embeds = [
            Embed.from_dict(SAPI.read("about")["embeds"][0]),
            Embed.from_dict(SAPI.read("about")["embeds"][1])
        ]
        buttons = [u"\u2B05", u"\u27A1"]
        current = 0

        # Send the initial contents.
        msg = await ctx.send(embeds = [embeds[current]])

        # Define the about parameters.
        for button in buttons:
            await msg.add_reaction(button)

        # Allow reactions to be added and check the logic for movements.
        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add",
                    check = lambda reaction, user: user == ctx.author and reaction.emoji in buttons,
                    timeout = 60
                )
            except TimeoutError:
                pass
            else:
                previous = current

                # Move backward if already forward.
                if reaction.emoji == buttons[0]:
                    current = 0

                # Move forward only if we're able to.
                elif reaction.emoji == buttons[1]:
                    current = 1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous:
                    await msg.edit(embed = embeds[current])

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
