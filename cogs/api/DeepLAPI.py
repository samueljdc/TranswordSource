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
        self.HTTP = f"https://api.depl.com/v2/translate?auth_key={auth}"
        self.headers = {
            "User-Agent": "YourApp",
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Define the languages we can translate/read.
        self.languages = {
            "source": ["DE", "EN", "FR", "IT", "JA", "ES", "NL", "PL", "PT", "RU", "ZH"],
            "target": ["DE", "EN-GB", "EN-US", "EN", "FR", "IT", "JA", "ES", "NL", "PL",
                       "PT-PT", "PT-BR", "PT", "RU", "ZH"]
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
            # Check if any of our target language won't work.
            if target == "":
                raise ScriptError(1000)
            elif target not in self.languages:
                raise ScriptError(1001)

            # Ensure HTTP request is safefully encoded.
            queries = "&text=".join(query) if isinstance(text, list) else text
            queries = queries.encode("utf-8")

            # Also look for any options to pass through, as well as the request details.
            options = "".join(f"&{opt[0]}={opt[1]}" for opt in types) if types != "" else ""
            encoded_url = requote_uri(f"{self.HTTP}{queries}&target_lang={target}{options}> HTTP/1.0")
            self.headers["Content-Length"] = getsizeof(queries)

            # Establish asynchronous connection to API.
            async with ClientSession(headers = self.headers) as session:
                # Check for any errors or fails.
                async with session.get(url = encoded_url) as error:
                    # Give us back the API's response with the status.
                    if self.parse_error(error.status):
                        raise HTTPError(code = resp, details = json(error)["message"])

                # Send the HTTP request off to the API.
                async with session.post(url = encoded_url) as data:
                    return json(data)["translations"][0]

        except ScriptError as exception:
            print(f"[DEEPLAPI] {exception}")

        sleep(3) # force delay to avoid 429 responses..
