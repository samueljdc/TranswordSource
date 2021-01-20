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
        self.cogs = []

        # Load the cogs.
        self.load_cogs()

    def load_cogs(self):
        """ Loads all of the cogs for the bot. """

        # Check for the directory itself.
        if __name__ == "__main__":
            for cog in self.cogs:
                print(f"[MAIN] Cog {cog} has been loaded.")

                cog_type = ""
                if "Comm" in cog:
                    cog_type = "cogs.commands"
                else:
                    pass

                self.bot.load_extension(f"{cog_type}.{cog}")
        else:
            pass

# Run the bot here.
transword = Transword()

@transword.bot.event
async def on_ready():
    """ Give us internal bot details once it's online. """

    # Some internal information variables being passed.
    time = datetime.now().strftime("%b %d %Y %H:%M:%S")

    # Put in a bot custom status.
    await transword.bot.change_presence(
        activity = CustomActivity("/help for commands.")
    )

    print(f"[MAIN] The bot is now online, passing details...")
    print(f"... Started: {time}")
    print("".join("=" for i in range(20)))


transword.bot.run(
    open(".TOKEN", "r").read(),
    bot = True,
    reconnect = True
)
