# 3rd party libraries
from discord import Embed
from discord.utils import get
from discord.ext import tasks
from discord.ext.commands import Cog
from dbl import DBLClient
from colorama import Fore, Back, Style, init
from asyncio import sleep

# Local libraries
from . import Errors

class TopAPI(Cog):
    """ Handle all of our HTTP information with Top.gg """

    def __init__(self,
                 bot):
        self.bot = bot
        self.token = open(".DBL", "r").read()
        self.API = DBLClient(
            self.bot,
            self.token,
            True,
            post_shard_count = True
        )

    def colored(self,
                text: str):
        """
            Allow colors to help format the Python terminal text to ease eyes.

            .colored("[[ERROR]][SLASHAPI][[END]] This fucked up!")
        """

        colors = {
            "ERROR": f"{Fore.WHITE}{Back.RED}{Style.BRIGHT}",
            "INFO": f"{Fore.WHITE}{Back.YELLOW}{Style.BRIGHT}",
            "END": f"{Fore.WHITE}{Back.BLACK}{Style.BRIGHT}"
        }

        for color in colors:
            text = text.replace(f"[[{color}]]", colors[color])

        return text

    @Cog.listener()
    async def on_guild_post(self):
        """ Update the Top.gg stats manually. """

        await self.API.post_guild_count()

def setup(bot):
    bot.add_cog(TopAPI(bot))
