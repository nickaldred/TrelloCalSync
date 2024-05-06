"""Sets up the API for the calendar sync service."""

from datetime import datetime
from os import environ
from typing import Optional
from config import Config, get_config
from dotenv import load_dotenv
from factorys import (
    calendar_handler_factory,
    db_handler_factory,
    board_webhook_handler_factory,
)
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google_calendar_handler import GoogleCalendarHandler
from trello_webhook_handler import TrelloWebhookHandler
from logging_funcs import log_decorator, log_error, log_info
from mongodb_handler import MongoDbHandler
from pydantic import BaseModel
from uvicorn import run

load_dotenv("./.env")

APP: FastAPI = FastAPI()
APP.add_middleware(
    CORSMiddleware,
    allow_origins=environ["API_ORIGINS"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CALENDAR_HANDLER: Optional[GoogleCalendarHandler] = calendar_handler_factory(
    environ.get("CALENDAR_TYPE")
)
BOARD_WEBHOOK_HANDLER: Optional[TrelloWebhookHandler] = (
    board_webhook_handler_factory(environ.get("BOARD_TYPE"))
)
DB_HANDLER: Optional[MongoDbHandler] = db_handler_factory(
    environ.get("DB_TYPE")
)
CONFIG: Config = get_config()


class Event(BaseModel):
    """The event model."""

    title: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str] = None
    calendar_id: str = "primary"
    card_id: str
    board_id: str
    current_status: str = "TO_DO"
    event_id: Optional[str] = None
    created_at: datetime = datetime.now()


class WebhookRequest(BaseModel):
    """Webhook request model."""

    action: dict
    model: dict
    webhook: dict


@APP.post("/add_event")
@log_decorator
def add_event(event: Event) -> dict:
    """Add an event to the calendar and database.

    Args:
        event (Event): The event to add.

    Returns:
        dict: The added event.
    """

    if not CALENDAR_HANDLER or not DB_HANDLER or not BOARD_WEBHOOK_HANDLER:
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
        BOARD_WEBHOOK_HANDLER.create_webhook(
            f"card_id-{event.card_id}-cal_id-{event.calendar_id}",
            environ["API_ENDPOINT_URL"],
            event.card_id,
        )

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
        event.card_id,
        event.board_id,
        event.event_id,
    )


@APP.head("/board_webhook/")
async def add_board_webhook() -> dict:
    """Set up the webhook.

    Returns:
        dict: The response.
    """
    log_info("Successfully set up board webhook")
    return {"message": "Webhook received successfully"}


@APP.post("/board_webhook/")
async def receive_board_webhook(web_hook_request: WebhookRequest) -> dict:
    """Receives the board webhooks.

    Args:
        web_hook_request (WebhookRequest): The webhook request.

    Returns:
        dict: The response.
    """
    log_info(f"Received webhook: {web_hook_request.model_dump()}")
    return {"message": "Webhook received successfully"}


@APP.post("/calendar_webhook/")
async def receive_calendar_webhook(
    x_goog_channel_id: str = Header(None),
    x_goog_channel_token: str = Header(None),
    x_goog_channel_expiration: str = Header(None),
    x_goog_resource_id: str = Header(None),
    x_goog_resource_uri: str = Header(None),
    x_goog_resource_state: str = Header(None),
    x_goog_message_number: int = Header(None),
    content_length: int = Header(None),
    content_type: str = Header(None),
):
    """Receives the calendar webhooks.

    Args:
        headers (WebhookHeaders): The webhook headers.
        content_type (str): The content type.

    Returns:
        dict: The response.
    """

    if content_type == "application/json; utf-8":
        # Handle JSON body here if needed
        pass
    else:
        print("Received Headers:")
        print(f"X-Goog-Channel-ID: {x_goog_channel_id}")
        print(f"X-Goog-Channel-Token: {x_goog_channel_token}")
        if x_goog_channel_expiration:
            print(f"X-Goog-Channel-Expiration: {x_goog_channel_expiration}")
        print(f"X-Goog-Resource-ID: {x_goog_resource_id}")
        print(f"X-Goog-Resource-URI: {x_goog_resource_uri}")
        print(f"X-Goog-Resource-State: {x_goog_resource_state}")
        print(f"X-Goog-Message-Number: {x_goog_message_number}")

    return {"message": "Notification received successfully"}


if __name__ == "__main__":
    # Test the API
    run(
        "cal_sync_api:APP",
        host=environ["API_HOST"],
        port=int(environ["API_PORT"]),
        log_level=environ["LOG_LEVEL"].lower(),
    )
