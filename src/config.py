"""Provides the configuration for the program."""

from dataclasses import dataclass
from json import load as json_load
from os import environ
from dotenv import load_dotenv

load_dotenv("./.env")


@dataclass
class Config:
    """Configuration for the program."""

    status: dict


def get_config() -> Config:
    """Gets the configuration for the program.

    Returns:
        Config: The configuration.
    """

    with open(environ["CONFIG_PATH"], "r", encoding="utf-8") as file:
        config_data: dict = json_load(file)

    return Config(**config_data)
