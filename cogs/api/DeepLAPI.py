# Imports libraries required.
import codecs
from typing import List
from requests.utils import requote_uri
from asyncio import sleep
from aiohttp import ClientSession, web.json_response as json

class DeepLError(Exception):
    """ Allows raising of different DeepL API errors. """

    def __init__(self,
                 *,
                 code: List[str, int],
                 details: str = None):
        # Set up a list of all possible API error codes.
        self.errors = {
            # API-specific errors.
            400: "Bad request. Please check error message and your parameters.",
            403: "Authorization failed. Please supply a valid auth_key parameter.",
            404: "The requested resource could not be found.",
            413: "The request size exceeds the limit.",
            429: "Too many requests. Please wait and resend your request.",
            456: "Quota exceeded. The character limit has been reached.",
            503: "Resource currently unavailable. Try again later.",
            "5**": "Internal error.",

            # Code-specific errors.
            1000: "No text was provided for the API to translate.",
            1001: "The target language specified does not exist."
        }

        if code not in self.errors:
            return False
        elif code >= 400 and code <= 503 or code == "5**":
            return f"{self.errors[error]} Additional details:\n\n{details}"
        else:
            return self.errors[error]

class DeepLAPI:
    """ API for handling all HTTP feedback to DeepL. """

    def __init__(self, auth):
        # Declare HTTP information variables.
        self.HTTP = f"https://api.depl.com/v2/translate?auth_key={auth}"
        self.headers = {
            "User-Agent": "YourApp",
            "Accept": "*/*",
            "Content-Length": 54, # what does this do? doesn't appear int-bsaed on char.
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
                        text: List[str, list],
                        target: str,
                        types: list = ""):

        """
            Translates one query/line of text to the specified language.

            .translate(
                text = ["Hello World.", "I allow multiple lines too!"],
                target = "DE",
                types = [["source_lang", "EN"], ["split_sentences", "0"]]
            )
        """

        try:
            # Check if any of our target language won't work.
            if target == "":
                raise DeepLError(code = 1000)
            elif target not in self.languages:
                raise DeepLError(code = 1001)

            # Ensure HTTP request is safefully encoded.
            queries = "&text=".join(query) if isinstance(text, list) else text
            options = "".join("&{opt[0]}={opt[1]}" for opt in types) if types != "" else ""
            encoded_url = requote_uri(f"{self.HTTP}{queries}&target_lang={target}{options}> HTTP/1.0")

            # Establish asynchronous connection to API.
            async with ClientSession(headers = self.headers) as session:
                # Check for any errors or fails.
                async with session.get(url = encoded_url) as error:
                    # Give us back the API's response with the status.
                    if self.parse_error(error.status):
                        raise DeepLError(code = resp, details = json(error)["message"])
                    else:
                        pass

                # Send the HTTP request off to the API.
                async with session.post(url = encoded_url) as data:
                    return json(data)["translations"][0]

        except DeepLError as exception:
            print(f"[DEEPLAPI] {exception}")

        sleep(3) # force delay to avoid 429 responses..
