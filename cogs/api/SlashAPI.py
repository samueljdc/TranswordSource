# 3rd party libraries
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import remove_slash_command, add_slash_command, get_all_commands
from json import loads
from typing import Union
from tinydb import TinyDB
from colorama import Fore, Back, Style, init

# Local libraries
from . import Errors

class SlashAPI(commands.Cog):
    """ API for handling all of the slash command utilization. """

    def __init__(self, bot):
        # Automatically reset the color formatting.
        init(autoreset = True)

        # Define some details of the bot.
        self.bot = bot
        self.details = {
            "token": open(".TOKEN", "r").read(),
            "id": 799697654279307314
        }

    def colored(self,
                text: str):
        """
            Allow colors to help format the Python terminal text to ease eyes.

            .colored("[[ERROR]][SLASHAPI][[END]] This fucked up!")
        """

        colors = {
            "ERROR": f"{Fore.WHITE}{Back.RED}{Style.BRIGHT}",
            "INFO": f"{Fore.WHITE}{Back.YELLOW}{Style.BRIGHT}",
            "END": f"{Fore.WHITE}{Back.BLUE}{Style.BRIGHT}"
        }

        for color in colors:
            text = text.replace(f"[[{color}]]", colors[color])

        return text

    def read(file: str,
             self = None) -> list:

        """
            Return information from a .JSON file.

            .read("join")
        """

        if file != "":
            colors = {
                "ERROR": f"{Fore.WHITE}{Back.RED}{Style.BRIGHT}",
                "INFO": f"{Fore.WHITE}{Back.YELLOW}{Style.BRIGHT}",
                "END": f"{Fore.WHITE}{Back.BLUE}{Style.BRIGHT}"
            }

            text = f"[[INFO]][SLASHAPI][[END]] Successfully read command [[INFO]]'{file}'[[END]] JSON contents."

            for color in colors:
                text = text.replace(f"[[{color}]]", colors[color])

            print(text)

            json = loads(open(f"cogs/commands/json/{file}.json", "r").read())
            return json
        else:
            raise Errors.ScriptError(1000)

    async def remove(self,
                     *,
                     guild_id: int = None,
                     cmd_id: int = None) -> int:

        """
            Removes a slash command from the Bot API.

            .remove(
                guild_id = 1234567890,
                cmd_id = 1234567890
            )
        """

        try:
            self.request = await remove_slash_command(
                self.details["id"],
                self.details["token"],
                guild_id,
                cmd_id
            )
        except error.RequestFailure as exception:
            print(self.colored(f"[[ERROR]][SLASHAPI][[END]] [[ERROR]]{exception}[[END]]"))

        if self.request == 204:
            print(self.colored(f"[[INFO]][SLASHAPI][[END]] Deletion of [[INFO]]{cmd_id}[[END]] was successful."))

        return self.request

    async def get(self, guild_id: int = None) -> list:

        """
            Get all of the slash commands from the Bot API.

            .get(1234567890)
        """

        try:
            self.request = await get_all_commands(
                self.details["id"],
                self.details["token"],
                guild_id
            )
        except error.RequestFailure as exception:
            print(self.colored(f"[[ERROR]][SLASHAPI][[END]] [[ERROR]]{exception}[[END]]"))

        if self.request == []:
            print(self.colored("[[INFO]][SLASHAPI][[END]] Command IDs found as empty."))
        else:
            amount = len(self.request)
            print(self.colored(f"[[INFO]][SLASHAPI][[END]] Command IDs found with [[INFO]]{amount}[[END]] entries."))

        return self.request

    async def create(self,
                     *,
                     guild_id: int = None,
                     cmd_name: str = "",
                     description: str = "",
                     options: list = None) -> list:

        """
            Creates a slash command from the Bot API.

            .create(
                guild_id = 1234567890,
                cmd_name = "test",
                description = "Nothing to see here!"
            )
        """

        try:
            try:
                if cmd_name != self.get(guild_id)["name"]:
                    self.request = await add_slash_command(
                        self.details["id"],
                        self.details["token"],
                        guild_id,
                        cmd_name,
                        description,
                        options
                    )

                    # Write a new command JSON entry with the request response.
                    TinyDB(f"commands/json/{cmd_name}.json").insert(self.request)
                else:
                    raise Errors.GatewayError(4005)
            except error.RequestFailure as exception:
                print(self.colored(f"[[ERROR]][SLASHAPI][[END]] [[ERROR]]{exception}[[END]]"))
        except GatewayError as exception:
            print(self.colored(f"[[ERROR]][SLASHAPI][[END]] [[ERROR]]{exception}[[END]]"))

        if self.request not in [[], None]:
            print(self.colored(f"[[INFO]][SLASHAPI][[END]] New slash command [[INFO]]\"{cmd_name}\"[[END]] successfully created."))

        return self.request

    # TODO: Find a way to create a modify function for the API that won't result in data loss/corruption for the JSON.

def setup(bot):
    bot.add_cog(SlashAPI(bot))
