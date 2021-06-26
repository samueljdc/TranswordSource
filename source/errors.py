# Normal libraries
from enum import Enum
import logging

# 3rd-party libraries
from discord.ext.commands import Cog
from discord_slash import SlashContext, ComponentContext

logging.basicConfig(filename="data/logs/Errors.log", level=logging.ERROR)

class Http(Enum):
    """Enumerable class for HTTP status codes."""
    BAD_REQUEST = 400
    AUTH_FAILED = 403
    REQ_NO_FIND = 404
    REQ_LIMITED = 413
    REQ_URL_BIG = 414
    RATED_LIMIT = 429
    REACHED_QUO = 456
    RES_UNAVAIL = 503
    REQ_TIMEOUT = 529

class HttpError(Exception):
    """
    Customized exception for handling HTTP errors.

    :ivar table: A list of acceptable status codes.

    :param message: The base message of the error.
    :type message: str
    :param status_code: The HTTP status code.
    :type message: int

    :return: str
    """
    def __init__(self,
                 *,
                 message: str,
                 status_code: int) -> str:
        self.table = {
            Http.BAD_REQUEST: "Bad request. Please check error message and your parameters.",
            Http.AUTH_FAILED: "Authorization failed. Please supply a valid auth_key parameter.",
            Http.REQ_NO_FIND: "The requested resource could not be found.",
            Http.REQ_LIMITED: "The request size exceeds the limit.",
            Http.REQ_URL_BIG: "The request URL is too long. You can avoid this error by using a POST request instead of a GET request.",
            Http.RATED_LIMIT: "Too many requests. Please wait and resend your request.",
            Http.REACHED_QUO: "Quota exceeded. The character limit has been reached.",
            Http.RES_UNAVAIL: "Resource currently unavailable. Try again later.",
            Http.REQ_TIMEOUT: "Too many requests. Please wait and resend your request.",
            "5**": "Internal error."
        }

        super().__init__(message + self.table[status_code])

class TranslateError(Exception):
    """
    Customized exception for handling DeepL translation errors.

    :param message: The base message of the error.
    :type message: str

    :return: str
    """
    def __init__(self,
                 *,
                 message: str) -> str:
        super().__init__(message)

class FeederError(Exception):
    """
    Customized exception for handling Feeder errors.

    :param message: The base message of the error.
    :type message: str

    :return: str
    """
    def __init__(self,
                 *,
                 message: str) -> str:
        super().__init__(message)

class BaseCommandError(Exception):
    """
    Customized exception for handling BaseCommand errors.

    :param message: The base message of the error.
    :type message: str

    :return: str
    """
    def __init__(self,
                 *,
                 message: str) -> str:
        super().__init__(message)

class BotErrors(Cog):
    """
    A bot cog that handles all of the listener events
    for bot errors.
    """
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_slash_command_error(self,
                                     ctx: SlashContext,
                                     error):
        print(error)
        return logging.error(error)

    @Cog.listener()
    async def on_component_callback_error(self,
                                          ctx: ComponentContext,
                                          error):
        print(error)
        return logging.error(error)

def setup(bot):
    bot.add_cog(BotErrors(bot))
