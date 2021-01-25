# Imports required API libraries.
from discord import Intents, Status, CustomActivity
from discord.ext import commands

# Imports additional libraries used.
from datetime import datetime

class Transword:
    """ Setup the bot information here. """

    def __init__(self):
        # Define the bot variables
        self.bot = commands.Bot(
            intents = Intents.all(),
            command_prefix = "/",
            help_command = None
        )
        self.cogs = ["Utils", "SlashAPI"]

        self.load_cogs()

    def load_cogs(self):
        """ Loads all of the cogs for the bot. """

        # Check for the directory itself.
        if __name__ == "__main__":
            for cog in self.cogs:
                cog_type = "cogs.api" if "API" in cog else "cogs.commands"

                self.bot.load_extension(f"{cog_type}.{cog}")
                print(f"[MAIN] Command {cog} has been loaded.")
        else:
            pass

# Run the bot here.
transword = Transword()

@transword.bot.event
async def on_ready():
    """ Give us internal bot details once it's online. """

    # Some internal information variables being passed.
    time = datetime.now().strftime("%b %d %Y %H:%M:%S")

    print(f"[MAIN] The bot is now online, passing details...")
    print(f"... Started: {time}")
    print("".join("=" for i in range(60))) # TODO: Re-write in more organized manner, very messy approach.


transword.bot.run(
    open(".TOKEN", "r").read(),
    bot = True,
    reconnect = True
)
