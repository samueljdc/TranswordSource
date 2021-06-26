# Normal libraries
from typing import Optional, Union
from json import loads, dump
from os.path import exists

# 3rd-party libraries
from .errors import BaseCommandError

class BaseCommand:
    """
    Class to be used for implementing base commands.
    This can be inferred on whenever needed.

    :ivar err: The base error string.
    :ivar name: The name of the command.
    :ivar description: The description of the command.
    :ivar options: The options the command may have.
    :ivar guild_ids: The guild IDs the command may register under.
    :ivar path: The JSON object path for reading the command contents.

    :param command_type: The type of command (regular/sub)
    :type command_type: str
    :param name: The name of the slash command.
    :type name: Union[str, dict]
    :param description: The slash command description.
    :type description: Optional[Union[str, dict]]
    :param options: Options for the slash command.
    :type options: Optional[list]
    :param guild_ids: A list of guilds to register under.
    :type guild_ids: Optional[list]

    :return: None
    """
    def __init__(self,
                 *,
                 command_type: str="regular",
                 name: Union[str, dict],
                 description: Optional[Union[str, dict]]="No description set.",
                 guild_ids: Optional[list]=[],
                 options: Optional[list]=[]) -> None:
        self.err: str = f"Could not instantiate {self.__class__.__name__}"
        self.name: Union[str, dict] = name
        self.description: Optional[Union[str, dict]] = description
        self.options: Optional[list] = options
        self.guild_ids: Optional[list] = guild_ids
        self.path: str = f"data/commands/{self.name}.json"

        try:
            if self.name == "":
                raise BaseCommandError(f"{self.err}: Command name is not given.")
            else:
                if exists(self.path):
                    self.model: dict = loads(open(self.path, "r").read())
                else:
                    with open(self.path, "w") as file:
                        if command_type == "regular":
                            dump({
                                "name": self.name,
                                "description": self.description,
                                "guild_ids": self.guild_ids,
                                "options": self.options
                            }, file)
                        elif command_type == "sub":
                            if isinstance(self.name, dict):
                                base: dict = {
                                    "main": self.name["base"],
                                    "desc": self.description["base"]
                                }
                                group: dict = {
                                    "main": self.name["group"],
                                    "desc": self.description["group"]
                                }
                                name: str = self.name["name"]
                                description: str = self.description["main"]

                            dump({
                                "base": base["main"],
                                "subcommand_group": group,
                                "name": name,
                                "description": description,
                                "base_description": base["desc"],
                                "subcommand_group_description": group["desc"],
                                "guild_ids": self.guild_ids,
                                "options": self.options
                            })
                    self.model: dict = loads(open(self.path, "r").read())
        except BaseCommandError as error:
            self.error(error=error)

    def error(self,
              *,
              error) -> BaseCommandError:
        """
        Returns the BaseCommandError class method.

        :param error: The error object.
        :type error: BaseCommandError

        :return: BaseCommandError
        """
        return error

class BaseSubcommand(BaseCommand):
    """
    Class to be used for implementing base subcommands.
    This already works off of the underlying logic of a
    regular base command but internally uses the proper
    keywords so dict conversion is made easier and little
    mitigation is made for developer programming.

    :inherit: BaseCommand
    """
    def __init__(self,
                 *,
                 name: dict,
                 description: dict,
                 guild_ids: Optional[list]=[],
                 options: Optional[list]=[]) -> None:
        super().__init__(
            command_type="sub",
            name=name,
            description=description,
            guild_ids=guild_ids,
            options=options
        )
