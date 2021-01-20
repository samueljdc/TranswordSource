# Imports required API libraries.
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands

class SlashAPI:
    """ API for handling all of the slash command utilization. """

    def __init__(self):
        # Define some details of the bot.
        self.details = {
            "token": open(".TOKEN", "r").read(),
            "id": self.bot.id
        }

    async def remove(self, **kwargs):
        """ Removes a slash command from the Bot API. """

        """
            .remove(
                guild_id = 1234567890,
                cmd_id = 1234567890
            )
        """

        try:
            # Assume global if no guild ID.
            if guild_id == None:
                self.request = await manage_commands.remove_slash_command(
                    self.details["id"],
                    self.details["token"],
                    None,
                    kwargs["cmd_id"]
                )
            else:
                self.request = await manage_commands.remove_slash_command(
                    self.details["id"],
                    self.details["token"],
                    kwargs["guild_id"],
                    kwargs["cmd_id"]
                )
        except error.RaiseError as exception:
            # Return the error if it fails.
            print(f"[SLASHAPI] {exception}")

        # Check to see if the request worked.
        if self.request == 204:
            print(f"[SLASHAPI] Deletion of {kwargs['cmd_id']} was successful.")
        else:
            pass

        # Pass off request information
        return self.request

    async def get(self, **kwarg):
        """ Get all of the slash commands from the Bot API. """

        """
            .get(guild_id = 1234567890)
        """

        try:
            # If we're getting global commands.
            if guild_id == None:
                self.request = await manage_commands.get_all_commands(
                    self.details["id"],
                    self.details["token"],
                    None
                )
            else:
                self.request = await manage_commands.get_all_commands(
                    self.details["id"],
                    self.details["token"],
                    kwarg["guild_id"]
                )
        except error.RaiseError as exception:
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
