# Normal libraries
from sys import getsizeof

# 3rd-party libraries
from typing import Optional, List, Union
from requests import get, post
from requests.utils import requote_uri
from json import loads
from .errors import Http, HttpError, TranslateError

class DeepL:
    """
    API for handling the HTTP requests' DeepL.

    :ivar err: The base error string.
    :type err: str
    :ivar base: The base HTTP route for the DeepL API.
    :type base: str
    :ivar http: A set of API endpoints.
    :type http: dict
    :ivar _auth: Stored instance for containing the API authorization key.
    :type _auth: str
    :ivar target_lang: A set of valid languages to translate to.
    :type target_lang: list
    :ivar source_lang: A set of valid languages to detect the source language from.
    :type source_lang: list
    :ivar split_sentences: Valid parameters for output formatting.
    :type split_sentences: list
    :ivar preserve_formatting: Valid parameters for formatting preservation.
    :type preserve_formatting: list
    :ivar formality: Valid parameters for informal/formal translating.
    :type formality: list

    :return: None
    """

    def __init__(self,
                 *,
                 auth: str,
                 lang_scope: Optional[
                    Union[str, bool]
                 ]=None) -> None:
        """
        Constructs the class method for the DeepL API.

        :param auth: The authentication key.
        :type auth: str
        :param lang_scope: The scope of the language to search.
        :type lang_scope: Optional[Union[str, bool]]

        :return: Optional[list]
        """
        self.err: str = f"Could not instantiate {self.__class__.__name__} class"
        self.base: str = "https://api.deepl.com/v2"
        self.http: dict = {
            "translate": f"{self.base}/translate?auth_key={auth}",
            "usage": f"{self.base}/usage?auth_key={auth}",
            "languages": f"{self.base}/languages"
        }
        self._auth: str = auth
        self.target_lang: list = [
            "BG",       "CS",       "DA", "DE", "EL",
            "EN-GB",    "EN-US",    "EN", "ES", "ET",
            "FI",       "FR",       "FU", "HU", "IT",
            "JA",       "LT",       "LV", "NL", "PL",
            "PT-PT",    "PT-BR",    "PT", "RO", "RU",
            "SK",       "SL",       "SV", "ZH"
        ]
        self.source_lang: list = [
            lang for lang in self.target_lang if lang not in
            ["EN-GB", "EN-US", "PT-PT", "PT-BR"]
        ]
        self.formal_exceptions: list = [
            "DE", "FR",     "IT",       "ES", "NL",
            "PL", "PT-PT",  "PT-BR",    "RU"
        ]
        self.split_sentences: list = ["0", "1", "newlines"]
        self.preserve_formatting: list = ["0", "1"]
        self.formality: list = ["default", "more", "less"]

    def request(self,
                *,
                scope: Optional[str]="translate",
                params: Optional[str]="") -> dict:
        """
        Sets up the base request method for DeepL synchronized HTTP.

        :param scope: The HTTP request scope.
        :type scope: Optional[str]
        :param params: The HTTP request parameters. (For querying)
        :type params: Optional[str]

        :return: dict
        """
        _scope = self.http[scope]
        encoded = requote_uri(_scope).replace("%0A", "")
        request = post(url=encoded)

        print("we're requesting now.")

        data = loads(response.content)
        if response.status_code != 200:
            try:
                if response.status_code in list(map(int, Http)):
                    print("poopy we got httperror")
                    raise HttpError(message=self.err, code=response.status_code)
                else:
                    error: str = data["message"]
                    print(f"some other error?\n{error}")
                    raise Exception(f"{self.err}: {error}")
            except HttpError as error:
                return error
        else:
            print("poggers")
            return data

    def is_valid(self) -> bool:
        """
        Checks to ensure that the auth key is valid.

        :return: bool
        """
        res = False
        print("trying valid")
        try:
            print("in valid try")
            proxy = self.request(scope=self.http["usage"])
            print(proxy.status_code)
            if self._auth == "":
                print("no auth :(")
                raise TranslateError(f"{self.err}: string is empty.")
            if proxy.status_code == 200:
                print("yes, it's valid")
                res = True
            if res:
                print("valid pog!!! :D")
                return res
        except TranslateError as error:
            print(error)
            return error


    def translate(self,
                  *,
                  text: str,
                  target_lang: str,
                  source_lang: Optional[str]=None,
                  split_sentences: Optional[Union[str, int]]=None,
                  preserve_formatting: Optional[Union[str, int]]=None,
                  formality: Optional[str]=None) -> dict:
        """
        Translates the text from an interpreted singular string.

        :param text: The text you want to translate.
        :type text: str
        :param target_lang: The language you wish to translate into.
        :type target_lang: str
        :param source_lang: The source language of the text.
        :type source_lang: Optional[str]
        :param split_sentences: If you would to format the sentences.
        :type split_sentences: Optional[Union[str, int]]
        :param preserve_formatting: If you would like to preserve the format.
        :type preserve_formatting: Optional[Union[str, int]]
        :param formality: If you would like your translation formal or informal.
        :type formality: Optional[str]

        :return: dict
        """
        _s_l = source_lang if isinstance(source_lang, str) else ["source_lang", None]
        _s_s = split_sentences if isinstance(split_sentences, (str, int)) else ["split_sentences", None]
        _p_f = preserve_formatting if isinstance(preserve_formatting, (str, int)) else ["preserve_formatting", None]
        _f = formality if isinstance(formality, str) else ["formality", None]

        try:
            for param in [_s_l, _s_s, _p_f, _f]:
                if param[1] != None:
                    if param[0] == "formality":
                        if target_lang in [
                            "EN",       "EN-GB", "EN-US",
                            "PT-PT",    "PT-BR", "ES",
                            "JA",       "ZH"
                        ]:
                            raise TranslateError(f"{self.err}: The target language entered does not support formality.")
                else:
                    payload.update({param[0]: param[1]})
            if text in ["", []]:
                raise TranslateError(f"{self.err}: The text to translate is empty.")
            if target_lang == "" or target_lang not in self.target_lang:
                raise TranslateError(f"{self.err}: The target language is either empty or does not exist.")
            else:
                payload.update({"target_lang": target_lang})

            path = f"&text={text}", "".join([f"&{payload}={param}" for param in payload])
            print(path)
            return self.request(params=path)
        except TranslateError as error:
            return error

    def usage(self) -> dict:
        """
        Returns back information about the API usage.

        :return: dict
        """
        return self.request(scope="usage")
