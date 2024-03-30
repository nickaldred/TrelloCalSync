"""Sets up the API for the calendar sync service."""

from os import environ
from typing import Optional
from config import Config, get_config
from data_models import Event
from dotenv import load_dotenv
from factorys import calendar_handler_factory, db_handler_factory
from fastapi import FastAPI, HTTPException
from google_calendar_handler import GoogleCalendarHandler
from logging_funcs import log_decorator, log_error, log_info
from mongodb_handler import MongoDbHandler
from uvicorn import run

load_dotenv("./.env")

APP: FastAPI = FastAPI()
CALENDAR_HANDLER: Optional[GoogleCalendarHandler] = calendar_handler_factory(
    environ.get("CALENDAR_TYPE")
)
DB_HANDLER: Optional[MongoDbHandler] = db_handler_factory(
    environ.get("DB_TYPE")
)
CONFIG: Config = get_config()


@APP.post("/add_event")
@log_decorator
def add_event(event: Event) -> dict:
    """Add an event to the calendar and database.

    Args:
        event (Event): The event to add.

    Returns:
        dict: The added event.
    """

    if not CALENDAR_HANDLER or not DB_HANDLER:
        error_msg: str = "Calendar or database handler not found"
        log_error(error_msg, item_id=event.card_id)
        raise HTTPException(status_code=400, detail=error_msg)

    event_id: Optional[str] = CALENDAR_HANDLER.add_event(
        event.title,
        event.description,
        event.start_datetime,
        event.end_datetime,
        CONFIG.get_status_colour_id(event.current_status),
        event.calendar_id,
        event.location,
    )
    event.event_id = event_id

    if event_id:
        db_result: bool = DB_HANDLER.add_document(
            "calendar_events", event.model_dump()
        )

        if db_result:
            log_info(
                "Successfully added calendar event to calendar and database",
                item_id=event.card_id,
            )
            return event.model_dump()

        else:
            error_msg = "Unable to add calendar event to database"
            log_error(error_msg, "database_error", item_id=event.card_id)
            CALENDAR_HANDLER.delete_event_by_id(event_id, event.calendar_id)
            raise HTTPException(status_code=400, detail=error_msg)

    else:
        error_msg = "Unable to add calendar event to calendar"
        log_error(error_msg, item_id=event.card_id)
        raise HTTPException(status_code=400, detail=error_msg)


@APP.get("/get_event/{event_id}")
@log_decorator
def get_event(trello_card_id: str) -> dict:
    """Get an event from the database.

    Args:
        trello_card_id (str): The Trello card ID.

    Returns:
        dict: The event.
    """

    if not DB_HANDLER or not CALENDAR_HANDLER:
        error_msg: str = "Calendar or database handler not found"
        log_error(error_msg, item_id=trello_card_id)
        raise HTTPException(status_code=400, detail=error_msg)

    event_data: dict = DB_HANDLER.get_document(
        "calendar_events", {"trello_card_id": trello_card_id}
    )

    calendar_event: dict = CALENDAR_HANDLER.get_event_by_id(
        event_data["event_id"], event_data["calendar_id"]
    )

    log_info(
        "Successfully retrieved event from calendar and database",
        item_id=trello_card_id,
    )
    return calendar_event


@APP.delete("/delete_event/{event_id}")
@log_decorator
def delete_event(trello_card_id: str) -> dict:
    """Delete an event from the calendar and database.

    Args:
        trello_card_id (str): The Trello card ID.

    Returns:
        dict: The deleted event.
    """
    if not DB_HANDLER or not CALENDAR_HANDLER:
        error_msg: str = "Calendar or database handler not found"
        log_error(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

    event_data: dict = DB_HANDLER.get_document(
        "calendar_events", {"trello_card_id": trello_card_id}
    )

    deleted_from_calendar: dict = CALENDAR_HANDLER.delete_event_by_id(
        event_data["event_id"], event_data["calendar_id"]
    )

    if deleted_from_calendar:
        deleted_event_data: bool = DB_HANDLER.delete_document(
            "calendar_events", {"trello_card_id": trello_card_id}
        )

        if deleted_event_data:
            log_info(
                "Successfully deleted calendar event from calendar "
                "and database",
                item_id=trello_card_id,
            )
            event_data["start_datetime"] = event_data[
                "start_datetime"
            ].isoformat()
            event_data["end_datetime"] = event_data["end_datetime"].isoformat()
            event_data["_id"] = str(event_data["_id"])

            return event_data

        else:
            error_msg = "Unable to delete calendar event from database"
            log_error(error_msg, item_id=trello_card_id)
            raise HTTPException(status_code=400, detail=error_msg)

    else:
        error_msg = "Unable to delete calendar event"
        log_error(error_msg, item_id=trello_card_id)
        raise HTTPException(status_code=400, detail=error_msg)


@APP.put("/update_event/{event_id}")
@log_decorator
def update_event(event_id: str, event: Event) -> dict:
    return CALENDAR_HANDLER.update_event_by_id(
        event_id,
        event.title,
        event.description,
        event.start_datetime,
        event.end_datetime,
        event.location,
        event.calendar_id,
        event.trello_card_id,
        event.trello_board_id,
        event.event_id,
    )


if __name__ == "__main__":
    # Test the API
    run(
        "cal_sync_api:APP",
        host=environ["API_HOST"],
        port=int(environ["API_PORT"]),
        log_level=environ["LOG_LEVEL"].lower(),
    )
