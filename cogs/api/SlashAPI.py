# Imports required API libraries.
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import remove_slash_command, add_slash_command, get_all_commands

# Imports additional libraries required.
from json import loads
from typing import Union
from tinydb import TinyDB
from . import Errors

class SlashAPI(commands.Cog):
    """ API for handling all of the slash command utilization. """

    def __init__(self, bot):
        # Define some details of the bot.
        self.bot = bot
        self.details = {
            "token": open(".TOKEN", "r").read(),
            "id": 799697654279307314
        }

    def read(file: str,
             self = None):

        """
            Return information from a .JSON file.

            .read("join")
        """

        if file == "":
            raise ScriptError(1000)
        else:
            json = loads(open(f"cogs/commands/json/{file}.json", "r").read())

            print(f"[SLASHAPI] Successfully read command \"{file}\" JSON contents.")
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
            try:
                # Let's make sure it doesn't exist.
                if cmd_name == self.get(guild_id)["name"]:
                    raise GatewayError(4005)
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
        except SlashError as exception:
            # Return the error if it fails.
            print(f"[SLASHAPI] {exception}")

        # Check for if the request passed or not.
        if self.request not in [[], None]:
            print(f"[SLASHAPI] New slash command \"{cmd_name}\" successfully created.")

        # Pass off request information
        return self.request

    # TODO: Find a way to create a modify function for the API that won't result in data loss/corruption for the JSON.

def setup(bot):
    bot.add_cog(SlashAPI(bot))
