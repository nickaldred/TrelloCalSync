"""Provides the configuration for the program."""

from dataclasses import dataclass
from json import load as json_load
from os import environ
from dotenv import load_dotenv

load_dotenv("./.env")


@dataclass
class Config:
    """Configuration for the program."""

    status_colour_ids: dict

    def get_status_colour_id(self, status_name: str) -> int:
        """Get the status colour id for a status.

        Args:
            status_name (str): The name of the status.

        Returns:
            dict: The status colour id.
        """

        if status_name in self.status_colour_ids:
            return self.status_colour_ids[status_name]
        else:
            print(
                f"Status {status_name} not found in config, "
                "using default status"
            )
            return self.status_colour_ids["DEFAULT"]


def get_config() -> Config:
    """Gets the configuration for the program.

    Returns:
        Config: The configuration.
    """

    with open(environ["CONFIG_PATH"], "r", encoding="utf-8") as file:
        config_data: dict = json_load(file)

    return Config(**config_data)
