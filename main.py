# Normal libraries
from time import sleep

def main():
    """Begins activation of the source."""
    from source import bot

    print("Starting the bot...")
    bot.run()

if __name__ == "__main__":
    logo = """ _______   _______  _______ .______    __
|       \ |   ____||   ____||   _  \  |  |
|  .--.  ||  |__   |  |__   |  |_)  | |  |
|  |  |  ||   __|  |   __|  |   ___/  |  |
|  '--'  ||  |____ |  |____ |  |      |  `----.
|_______/ |_______||_______|| _|      |_______|
                                               """
    print(logo)
    main()
