# Standard libraries
import codecs
from sys import getsizeof

# 3rd party libraries
from typing import Union
from requests import get, post
from requests.utils import requote_uri
from json import loads
from colorama import Fore, Back, Style, init

# Local libraries
from . import Errors

class DeepLAPI:
    """ API for handling all HTTP feedback to DeepL. """

    def __init__(self, auth):
        # Declare HTTP information variables.
        self.HTTP = {
            "translate": f"https://api.deepl.com/v2/translate?auth_key={auth}",
            "usage": f"https://api.deepl.com/v2/usage?auth_key={auth}"
        }
        self.headers = {
            "Host": "api.deepl.com",
            "User-Agent": "Transword",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Specify all target languages accessible.
        self.target = ["DE", "EN-GB", "EN-US",
                       "EN", "FR", "IT", "JA",
                       "ES", "NL", "PL", "PT-PT",
                       "PT-BR", "PT", "RU", "ZH"]

        # Define the options that can exist for translations.
        self.options = {
            "source_lang": ["DE", "EN", "FR",
                            "IT", "JA", "ES",
                            "NL", "PL", "PT",
                            "RU", "ZH"],
            "split_sentences": ["0", "1", "nonewlines"],
            "preserve_formatting": ["0", "1"],
            "formality": ["default", "more", "less"]
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

    def translate(self,
                  *,
                  text: Union[str, list],
                  target: str,
                  types: list = "") -> dict:

        """
            Translates one query/line of text to the specified language.

            .translate(
                text = [
                    "Hello World.",
                    "I allow multiple lines too!"
                ],
                target = "DE",
                types = [
                    ["source_lang", "EN"],
                    ["split_sentences", "0"],
                    ["formality", "less"]
                ]
            )
        """

        # Check if any of our arguments are void.
        if text in [[], ""]:
            raise Errors.ScriptError(1001)
        if target not in self.target:
            raise Errors.ScriptError(1002)

        # Ensure HTTP request is safefully encoded.
        queries = f"text={text}"

        if isinstance(text, list):
            if len(text) <= 50:
                queries = "&text=".join(query)
            else:
                raise Errors.HTTPError(413)

        # Do some format checks if options do exist.
        options = types

        if options != "":
            options = "".join(f"&{opt[0]}={opt[1]}" for opt in types)

            for opt in types:
                # Have to keep this all str-based!
                if not isinstance(opt[0], str):
                    opt[0] = str(opt[0])
                if not isinstance(opt[1], str):
                    opt[1] = str(opt[1])
                if opt[0] not in self.options:
                    raise Errors.ScriptError(1003)
                elif opt[0] == "formality":
                    # If formality is on but language is in the exception list.
                    if target in ["EN", "EN-GB", "EN-US",
                                  "ES", "JA", "ZH"]:
                        raise Errors.HTTPError(503)
                else:
                    if opt[1] not in self.options[opt[0]]:
                        raise Errors.ScriptError(1004)

        # Encode the URI path to be ready for request sending.
        encoded_url = requote_uri(f"{self.HTTP['translate']}&{queries}&target_lang={target.lower()}{options}").replace("%0A", "")

        # Give back some information.
        print(self.colored(f"[[INFO]][DEEPLAPI][[END]] Translation request is being attempted now..."))
        print(self.colored(f"[[END]]... Path: {encoded_url}\n... Target: {target}\n... Text: {text}\n... Options: {options}[[END]]"))

        # Establish asynchronous connection to API and determine states.
        error = get(url = encoded_url)

        if error:
            return loads(error.content)
        else:
            data = get(url = encoded_url)
            return loads(data.content)

    def usage(self):
        """
            Collects statistics of the bot's usage.

            .usage()
        """

        # Encode the URI path to be ready for request sending.
        encoded_url = requote_uri(f"{self.HTTP['usage']}").replace("%0A", "")

        # Give back some information.
        print(self.colored(f"[[INFO]][DEEPLAPI][[END]] Statistics request is being attempted now..."))
        print(self.colored(f"[[END]]... Path: {encoded_url}[[END]]"))

        # Establish asynchronous connection to API and determine states.
        error = get(url = encoded_url)

        if error:
            return loads(error.content)
        else:
            data = get(url = encoded_url)
            return loads(data.content)
