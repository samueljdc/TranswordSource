# Imports required API libraries.
import discord
from discord import Intents, Status, Activity, ActivityType
from discord.ext import commands
from discord_slash import SlashCommand

# Imports additional libraries used.
from datetime import datetime
from colorama import Fore, Back, Style, init, ansi
from os import system

class Transword:
    """ Setup the bot information here. """

    def __init__(self):
        # Handle all terminal formatting.
        init()
        system("title Transword - Bot Terminal")

        # print(f"{Fore.WHITE}{Back.BLUE}{Style.BRIGHT}")
        print(ansi.clear_screen())

        # Define the bot variables.
        self.bot = commands.Bot(
            intents = Intents.all(),
            command_prefix = "prefix",
            help_command = None
        )
        self.slash = SlashCommand(
            self.bot,
            override_type = True,
            sync_commands = True
        )
        self.cogs = ["Utils", "Translation", "SlashAPI"]

        print("""  ______                                              __
 /_  __/________ _____  ______      ______  _________/ /
  / / / ___/ __ `/ __ \/ ___/ | /| / / __ \/ ___/ __  /
 / / / /  / /_/ / / / (__  )| |/ |/ / /_/ / /  / /_/ /
/_/ /_/   \__,_/_/ /_/____/ |__/|__/\____/_/   \__,_/
                                                        """)
        print("".join("-" for i in range(56)))

        self.load_cogs()

    def colored(self, text: str):
        """ Allow colors to help format the Python terminal text to ease eyes. """

        colors = {
            "ERROR": f"{Fore.WHITE}{Back.RED}{Style.BRIGHT}",
            "INFO": f"{Fore.WHITE}{Back.YELLOW}{Style.BRIGHT}",
            "END": f"{Fore.WHITE}{Back.BLACK}{Style.RESET_ALL}"
        }

        for color in colors:
            text = text.replace(f"[[{color}]]", colors[color])

        return text

    def load_cogs(self):
        """ Loads all of the cogs for the bot. """

        # Check for the directory itself.
        if __name__ == "__main__":
            for cog in self.cogs:
                cog_type = "cogs.api" if "API" in cog else "cogs.commands"

                self.bot.load_extension(f"{cog_type}.{cog}")
                print(self.colored(f"[[INFO]][MAIN][[END]] Command [[INFO]]{cog}[[END]] has been loaded."))
        else:
            pass

# Run the bot here.
transword = Transword()

@transword.bot.event
async def on_ready():
    """ Give us internal bot details once it's online. """

    # Some internal information variables being passed.
    time = datetime.now().strftime("%b %d %Y %H:%M:%S")
    servers = len(transword.bot.guilds)

    prints = [
        f"[[INFO]][MAIN][[END]] The bot is now online, passing details...",
        f"[[END]]... Started: [[INFO]]{time}[[END]]",
        f"[[END]]... Server Count: [[INFO]]{servers}[[END]]",
        f"[[END]]... Discord.py Version: [[INFO]]{discord.__version__}[[END]]",
        f"[[END]]... Slash Version: [[INFO]]1.0.9.4[[END]]"
    ]

    for line in prints:
        print(transword.colored(line))

    print(transword.colored("[[END]]" + "".join("-" for i in range(56))))

    # Set up the custom status.
    await transword.bot.change_presence(
        status = Status.idle,
        activity = Activity(
            name = "for /help",
            type = ActivityType.watching
        )
    )


transword.bot.run(
    open(".TOKEN", "r").read(),
    bot = True,
    reconnect = True
)
