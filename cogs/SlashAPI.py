# Imports required API libraries.
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils import manage_commands

class SlashAPI(commands.Cog):
    """ API for handling all of the slash command utilization. """

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
        """ Removes the original cog context from d.py. """

        self.bot.slash.remove_cog_commands(self)

    async def remove(self, guild_id: int, cmd_id: int):
        """ Removes a slash command from the Bot API. """

        try:
            # Assume global if no guild ID.
            if guild_id == None:
                self.request = await manage_commands.remove_slash_command(
                    self.bot.id,
                    open(".TOKEN", "r").read(),
                    None,
                    cmd_id
                )
            else:
                self.request = await manage_commands.remove_slash_command(
                    self.bot.id,
                    open(".TOKEN", "r").read(),
                    guild_id,
                    cmd_id
                )
        except error.RaiseError as exception:
            # Return the error if it fails.
            print(f"[SLASHAPI] {exception}")

        # Check to see if the request worked.
        if self.request == 204:
            print(f"[SLASHAPI] Deletion of {cmd_id} was successful.")
        else:
            pass

    async def get(self, guild_id: int):
        """ Get all of the slash commands from the Bot API. """

        try:
            # If we're getting global commands.
            if guild_id == None:
                self.request = await manage_commands.get_all_commands(
                    self.bot.id,
                    open(".TOKEN", "r").read(),
                    None
                )
            else:
                self.request = await manage_commands.get_all_commands(
                    self.bot.id,
                    open(".TOKEN", "r").read(),
                    guild_id
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

def setup(bot):
    bot.add_cog(SlashAPI(bot))
