"""Factory functions for creating handlers."""

from typing import Optional
from exceptions import FactoryError
from google_calendar_handler import GoogleCalendarHandler
from mongodb_handler import MongoDbHandler
from trello_handler import TrelloHandler


def calendar_handler_factory(
    type_of_handler: str,
) -> Optional[GoogleCalendarHandler]:
    """Create a calendar handler.

    Args:
        type_of_handler (str): The type of calendar handler to create.

    Returns:
        GoogleCalendarHandler: The calendar handler.
    """
    if type_of_handler == "google":
        return GoogleCalendarHandler(
            scopes=[
                "https://www.googleapis.com/auth/calendar",
            ],
            token_file_path="token.json",
            service_account_file_path="credentials.json",
        )
    else:
        raise FactoryError("Invalid calendar handler type")


def db_handler_factory(type_of_handler: str) -> Optional[MongoDbHandler]:
    """Create a database handler.

    Args:
        type_of_handler (str): The type of database handler to create.

    Returns:
        MongoDbHandler: The database handler.
    """
    if type_of_handler == "mongo":
        return MongoDbHandler(host="localhost", port=27017, db_name="cal_sync")
    else:
        raise FactoryError("Invalid database handler type")
