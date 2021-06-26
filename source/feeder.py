# Normal libraries
from json import loads, dump
from configparser import ConfigParser
from typing import Union
import logging

# 3rd-party libraries
from .errors import FeederError

logging.basicConfig(filename="data/logs/Feeder.log", level=logging.INFO)

class Feeder:
    """
    A file reading class that simplifies parsing configuration files.

    This already works off of the basis of the ConfigParser class method,
    but is boiled down into a few methods that help me keep my sanity
    whenever I am writing my code revisions at 4 AM in the morning.

    Yes, I am aware of the fact that this class is almost entirely pointless.
    Too bad!
    Godspeed and help me.

    :ivar err: The base error string.
    :ivar config: The configuration loader.

    :return: None
    """
    def __init__(self) -> None:
        self.err = f"Could not instantiate {self.__class__.__name__} class"
        self.config = ConfigParser()

    def read_token(self,
                   *,
                   key: str) -> Union[str, int, bool]:
        """
        Reads the main access.ini file from the data/ directory
        and returns the value of a given key.

        :param key: The name of the key to access.
        :type key: str

        :return: Union[str, int, bool]
        """
        try:
            self.config.read("data/access.ini")
            for section in self.config.sections():
                if section == "API":
                    val = self.config[section][key]
                    if val not in ["", 0, False]:
                        return val
                    else:
                        raise FeederError(message=f"{self.err}: Given key '{key}' does not exist or nothing found.")
        except FeederError as error:
            return error
