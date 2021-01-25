# Imports libraries required.
import codecs
from sys import getsizeof
from typing import Union
from requests.utils import requote_uri
from asyncio import sleep
from aiohttp import ClientSession, web.json_response as json
from . import Errors

class DeepLAPI:
    """ API for handling all HTTP feedback to DeepL. """

    def __init__(self, auth):
        # Declare HTTP information variables.
        self.HTTP = f"https://api.deepl.com/v2/translate?auth_key={auth}"
        self.headers = {
            "User-Agent": "YourApp",
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

    async def translate(self,
                        *,
                        text: Union[str, list],
                        target: str,
                        types: list = ""):

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

        try:
            # Check if any of our arguments are void.
            if text in [[], ""]:
                raise ScriptError(1001)
            if target not in self.target:
                raise ScriptError(1002)

            # Ensure HTTP request is safefully encoded.
            queries = text

            if isinstance(text, list):
                if len(text) <= 50:
                    queries = "&text=".join(query)
                else:
                    raise HTTPError(413)

            queries = queries.encode("utf-8")

            # Do some format checks if options do exist.
            if types != "":
                options = "".join(f"&{opt[0]}={opt[1]}" for opt in types)

                for opt in types:
                    if opt[0] not in self.options:
                        raise ScriptError(1003)
                    elif opt[0] == "formality":
                        # If formality is on but language is in the exception list.
                        if target in ["EN", "EN-GB", "EN-US",
                                      "ES", "JA", "ZH"]:
                            raise HTTPError(503)
                    else:
                        if opt[1] not in self.options[opt]:
                            raise ScriptError(1004)

            # Encode the URI path to be ready for request sending.
            encoded_url = requote_uri(f"{self.HTTP}{queries}&target_lang={target}{options}> HTTP/1.0")
            self.headers["Content-Length"] = getsizeof(queries)

            # Establish asynchronous connection to API and determine states.
            async with ClientSession(headers = self.headers) as session:
                async with session.get(url = encoded_url) as error:
                    if self.parse_error(error.status):
                        raise HTTPError(code = resp, details = json(error)["message"])
                async with session.post(url = encoded_url) as data:
                    return json(data)["translations"][0]
        except ScriptError as exception:
            print(f"[DEEPLAPI] {exception}")

        sleep(3) # force delay to avoid 429 responses..
