# Imports required API libraries.
import requests

# Imports additional libraries required.
from typing import List, Union

class DeepLError(Exception):
    """ Allows raising of different DeepL API errors. """

    def __init__(self, error):
        # Set up a list of all possible API error codes.
        self.errors = {
            400: "Bad request. Please check error message and your parameters.",
            403: "Authorization failed. Please supply a valid auth_key parameter.",
            404: "The requested resource could not be found.",
            413: "The request size exceeds the limit.",
            429: "Too many requests. Please wait and resend your request.",
            456: "Quota exceeded. The character limit has been reached.",
            503: "Resource currently unavailable. Try again later.",
            "5xx": "Internal error"
        }

        return self.errors[error]

class DeepLAPI:
    """ API for handling all HTTP feedback to DeepL. """

    def __init__(self, auth):
        # Declare HTTP information variables.
        self.HTTP = f"https://api.depl.com/v2/usage?auth_key=[{auth}]> HTTP/1.0"
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

    def parse_error(self, error: Union[str, int]):
        """ Passes off an error type from the list. """

        raise DeepLError(error)

    def translate_small(self,
                        *,
                        text: str,
                        target: str,
                        **types):
        """ Translates one query/line of text to the specified language. """

        try:
            pass
        except DeepLError as error:
            self.parse_error(error)

    def translate_large(self,
                        *,
                        text: List[str],
                        target: str,
                        **types):
        """ Translates large volumes/queries of text to the specified language. """

        try:
            pass
        except DeepLError as error:
            self.parse_error(error)
