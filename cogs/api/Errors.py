# Imports libraries required.
from typing import Union

class APIFailure(Exception):
    """ Allows raising of different API errors. """

class JSONError(APIFailure):
    """ A JSON-specific error has been triggered. """

    def __init__(self, error: Union[str, int]):
        self.errors = {
            400: "The request was improperly formatted, or the server couldn't understand it.",
            401: "The Authorization header was missing or invalid.",
            403: "The Authorization token you passed did not have permission to the resource.",
            404: "The resource at the location specified doesn't exist.",
            405: "The HTTP method used is not valid for the location specified.",
            429: "You are being rate limited, see Rate Limits.",
            502: "There was not a gateway available to process your request. Wait a bit and retry.",
            "5xx": "The server had an error processing your request.",
        }

        super().__init__(self.errors[error])

class ScriptError(APIFailure):
    """ A code-specific error has been triggered. """

    def __init__(self, error: int):
        self.errors = {
            # SlashAPI
            1000: "JSON Read unsuccessful, file could not be found.",

            # DeepLAPI
            1001: "No text was provided for the API to translate.",
            1002: "The target language specified does not exist."
        }

        super().__init__(self.errors[error])

class GatewayError(APIFailure):
    """ A gateway-specific error has been triggered. """

    def __init__(self, error: int):
        self.errors = {
            4005: "You sent more than one identify payload.",
        }

        super().__init__(self.errors[error])

class HTTPError(APIFailure):
    """ A DeepL API-specific error has been triggered. """

    def __init__(self,
                 *,
                 code: Union[str, int],
                 details: str = None):
        self.errors = {
            400: "Bad request. Please check error message and your parameters.",
            403: "Authorization failed. Please supply a valid auth_key parameter.",
            404: "The requested resource could not be found.",
            413: "The request size exceeds the limit.",
            429: "Too many requests. Please wait and resend your request.",
            456: "Quota exceeded. The character limit has been reached.",
            503: "Resource currently unavailable. Try again later.",
            "5**": "Internal error."
        }

        if code not in self.errors:
            return False
        else:
            super().__init__(f"{self.errors[error]} Additional details:\n\n{details}")
