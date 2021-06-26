# 3rd-party libraries
from discord.ext.commands import Cog
from discord_slash import SlashContext
from discord_slash.cog_ext import cog_slash
from discord_slash.model import SlashCommandOptionType as opt_type
from ..model import BaseCommand

base = BaseCommand(
    name="test",
    guild_ids=[799685484313968670],
    options=[
        dict(name="option_one", description="This is an option", type=opt_type.STRING, required=True)
    ]
)

class Test(Cog):
    """
    A test command for the bot.
    Relies off of the BaseCommand class for construction.
    """
    def __init__(self,
                 bot) -> None:
        self.bot = bot

    @cog_slash(**base.model)
    async def command(self,
                      ctx: SlashContext,
                      option_one: str) -> None:
        await ctx.send(content=option_one)

def setup(bot):
    bot.add_cog(Test(bot))
