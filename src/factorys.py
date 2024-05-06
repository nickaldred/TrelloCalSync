"""Factory functions for creating handlers."""

from ast import literal_eval
from os import environ
from typing import Optional
from dotenv import load_dotenv
from exceptions import FactoryError
from google_calendar_handler import GoogleCalendarHandler
from logging_funcs import debug_log_decorator
from mongodb_handler import MongoDbHandler
from trello_handler import TrelloHandler
from trello_webhook_handler import TrelloWebhookHandler
from google_webhook_handler import GoogleWebhookHandler

load_dotenv("./.env")


@debug_log_decorator
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
            scopes=literal_eval(environ["CALENDAR_SCOPES"]),
            token_file_path=environ["CALENDAR_TOKEN_FILE_PATH"],
            service_account_file_path=environ[
                "CALENDAR_SERVICE_ACCOUNT_FILE_PATH"
            ],
        )
    else:
        raise FactoryError("Invalid calendar handler type")


@debug_log_decorator
def db_handler_factory(type_of_handler: str) -> Optional[MongoDbHandler]:
    """Create a database handler.

    Args:
        type_of_handler (str): The type of database handler to create.

    Returns:
        MongoDbHandler: The database handler.
    """
    if type_of_handler == "mongo":
        return MongoDbHandler(
            host=environ["DB_HOST"],
            port=int(environ["DB_PORT"]),
            db_name=environ["DB_NAME"],
        )
    else:
        raise FactoryError("Invalid database handler type")


@debug_log_decorator
def board_handler_factory(type_of_handler: str) -> Optional[TrelloHandler]:
    """Create a board handler.

    Args:
        type_of_handler (str): The type of board handler to create.

    Returns:
        TrelloHandler: The board handler.
    """
    if type_of_handler == "trello":
        return TrelloHandler(
            api_key=environ["BOARD_API_KEY"],
            api_secret=environ["BOARD_API_SECRET"],
            token=environ["BOARD_TOKEN"],
        )
    else:
        raise FactoryError("Invalid board handler type")


@debug_log_decorator
def board_webhook_handler_factory(
    type_of_handler: str,
) -> Optional[TrelloWebhookHandler]:
    """Create a webhook handler.

    Args:
        type_of_handler (str): The type of webhook handler to create.

    Returns:
        TrelloWebhookHandler: The webhook handler.
    """
    if type_of_handler == "trello":
        return TrelloWebhookHandler(
            api_key=environ["BOARD_API_KEY"],
            token=environ["BOARD_TOKEN"],
        )
    else:
        raise FactoryError("Invalid webhook handler type")


@debug_log_decorator
def calendar_webhook_handler_factory(
    type_of_handler: str,
) -> Optional[GoogleWebhookHandler]:
    """Create a webhook handler.

    Args:
        type_of_handler (str): The type of webhook handler to create.

    Returns:
        GoogleCalendarHandler: The webhook handler.
    """
    if type_of_handler == "google":
        return GoogleWebhookHandler(
            scopes=literal_eval(environ["CALENDAR_SCOPES"]),
            token_file_path=environ["CALENDAR_TOKEN_FILE_PATH"],
            service_account_file_path=environ[
                "CALENDAR_SERVICE_ACCOUNT_FILE_PATH"
            ],
        )
    else:
        raise FactoryError("Invalid webhook handler type")


if __name__ == "__main__":
    # handler = board_handler_factory("trello")
    # print(handler.get_all_lists("61ec0eaf3ad6121bee980f38"))

    cal_handler = calendar_handler_factory("google")
    print(cal_handler.get_todays_events())
