# Imports required API libraries.
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import remove_slash_command, add_slash_command, get_all_commands

# Imports additional libraries required.
from json import loads
from typing import Union
from tinydb import TinyDB

class SlashError(Exception):
    """ Allows raising of different Slash API errors. """

    def __init__(self, error):
        # Set up a list of all possible API error codes.
        self.errors = {
            # JSON Codes
            400: "The request was improperly formatted, or the server couldn't understand it.",
            401: "The Authorization header was missing or invalid.",
            403: "The Authorization token you passed did not have permission to the resource.",
            404: "The resource at the location specified doesn't exist.",
            405: "The HTTP method used is not valid for the location specified.",
            429: "You are being rate limited, see Rate Limits.",
            502: "There was not a gateway available to process your request. Wait a bit and retry.",
            "5xx": "The server had an error processing your request.",

            # Gateway Codes
            4005: "You sent more than one identify payload."
        }

        return self.errors[error]

class SlashAPI(commands.Cog):
    """ API for handling all of the slash command utilization. """

    def __init__(self, bot):
        # Define some details of the bot.
        self.bot = bot
        self.details = {
            "token": open(".TOKEN", "r").read(),
            "id": 799697654279307314
        }

    def parse_error(self,
                    error: Union[str, int]):

        """ Passes off an error type from the list. """

        raise SlashError(error)

    def read(self,
             file: str):

        """
            Return information from a .JSON file.

            .read("join")
        """

        json = loads(open(f"cogs/commands/json/{file}.json", "r").read())
        return json

    async def remove(self,
                     *,
                     guild_id: int = None,
                     cmd_id: int = None):

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
            # Return the error if it fails.
            print(f"[SLASHAPI] {exception}")

        # Check to see if the request worked.
        if self.request == 204:
            print(f"[SLASHAPI] Deletion of {cmd_id} was successful.")
        else:
            pass

        # Pass off request information
        return self.request

    async def get(self, guild_id: int = None):

        """
            Get all of the slash commands from the Bot API.

            .get(1234567890)
        """

        try:
            # Make the HTTP request to get all of the commands.
            self.request = await get_all_commands(
                self.details["id"],
                self.details["token"],
                guild_id
            )
        except error.RequestFailure as exception:
            # Return the error if it fails.
            print(f"[SLASHAPI] {exception}")

        # Check if the list is empty
        if self.request == []:
            print("[SLASHAPI] Command IDs found as empty.")
        else:
            amount = len(self.request)
            print(f"[SLASHAPI] Command IDs found with {amount} entries.")

        # Pass off request information
        return self.request

    async def create(self,
                     *,
                     guild_id: int = None,
                     cmd_name: str = "",
                     description: str = "",
                     options: list = None):

        """
            Creates a slash command from the Bot API.

            .create(
                guild_id = 1234567890,
                cmd_name = "test",
                description = "Nothing to see here!"
            )
        """

        try:
            # Let's make sure it doesn't exist.
            if cmd_name == self.get(guild_id)["name"]:
                self.parse_error(4005)
            else:
                # Make the HTTP request to add a command.
                self.request = await add_slash_command(
                    self.details["id"],
                    self.details["token"],
                    guild_id,
                    cmd_name,
                    description,
                    options
                )

                # Write a new command JSON entry with the request response
                TinyDB(f"commands/json/{cmd_name}.json").insert(self.request)
        except error.RequestFailure as exception:
            # Return the error if it fails.
            print(f"[SLASHAPI] {exception}")

        # Check for if the request passed or not.
        if self.request in [[], None]:
            pass
        else:
            print(f"[SLASHAPI] New slash command \"{cmd_name}\" successfully created.")

        # Pass off request information
        return self.request

def setup(bot):
    bot.add_cog(SlashAPI(bot))
