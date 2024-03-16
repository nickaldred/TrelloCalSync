"""Sets up the API for the calendar sync service."""

from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from google_calendar_handler import GoogleCalendarHandler
from mongodb_handler import MongoDbHandler
from pydantic import BaseModel
from uvicorn import run

app: FastAPI = FastAPI()


class ApiError(Exception):
    """The base class for API errors."""

    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)


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
        raise ApiError("Invalid calendar handler type")


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
        raise ApiError("Invalid database handler type")


calendar_handler: Optional[GoogleCalendarHandler] = calendar_handler_factory(
    "google"
)
db_handler: Optional[MongoDbHandler] = db_handler_factory("mongo")


class Event(BaseModel):
    """The event model."""

    title: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str] = None
    calendar_id: str = "primary"
    trello_card_id: str
    trello_board_id: str
    event_id: Optional[str] = None
    created_at: datetime = datetime.now()


@app.post("/add_event")
def add_event(event: Event) -> dict:
    """Add an event to the calendar and database.

    Args:
        event (Event): The event to add.

    Returns:
        dict: The added event.
    """

    if not calendar_handler or not db_handler:
        raise HTTPException(
            status_code=400, detail="Calendar or database handler not found"
        )

    event_id: Optional[str] = calendar_handler.add_event(
        event.title,
        event.description,
        event.start_datetime,
        event.end_datetime,
        event.location,
        event.calendar_id,
    )
    event.event_id = event_id

    if event_id:
        db_result: bool = db_handler.add_document(
            "calendar_events", event.model_dump()
        )

        if db_result:
            print("Successfully added calendar event to calendar and database")
            return event.model_dump()
        else:
            print(
                "Unable to add calendar event to database, "
                "removing from calendar"
            )
            calendar_handler.delete_event_by_id(event_id, event.calendar_id)
            raise HTTPException(
                status_code=400,
                detail="Event not added, unable to add to database",
            )
    else:
        print("Unable to add calendar event to calendar")
        raise HTTPException(
            status_code=400,
            detail="Event not added, unable to add to calendar",
        )


@app.get("/get_event/{event_id}")
def get_event(trello_card_id: str) -> dict:
    """Get an event from the database.

    Args:
        trello_card_id (str): The Trello card ID.

    Returns:
        dict: The event.
    """

    if not db_handler or not calendar_handler:
        raise HTTPException(
            status_code=400, detail="Calendar or database handler not found"
        )

    event_data: dict = db_handler.get_document(
        "calendar_events", {"trello_card_id": trello_card_id}
    )

    calendar_event: dict = calendar_handler.get_event_by_id(
        event_data["event_id"], event_data["calendar_id"]
    )

    return calendar_event


@app.delete("/delete_event/{event_id}")
def delete_event(trello_card_id: str) -> dict:
    """Delete an event from the calendar and database.

    Args:
        trello_card_id (str): The Trello card ID.

    Returns:
        dict: The deleted event.
    """
    if not db_handler or not calendar_handler:
        raise HTTPException(
            status_code=400, detail="Calendar or database handler not found"
        )

    event_data: dict = db_handler.get_document(
        "calendar_events", {"trello_card_id": trello_card_id}
    )

    deleted_from_calendar: dict = calendar_handler.delete_event_by_id(
        event_data["event_id"], event_data["calendar_id"]
    )

    print(f"deleted_from_calendar: {deleted_from_calendar}")
    if deleted_from_calendar:
        deleted_event_data: bool = db_handler.delete_document(
            "calendar_events", {"trello_card_id": trello_card_id}
        )

        if deleted_event_data:
            print("Successfully deleted event from calendar and database")
            event_data["start_datetime"] = event_data[
                "start_datetime"
            ].isoformat()
            event_data["end_datetime"] = event_data["end_datetime"].isoformat()
            event_data["_id"] = str(event_data["_id"])

            return event_data
        else:
            raise HTTPException(
                status_code=400,
                detail="Event not deleted, unable to delete from database",
            )
    else:
        raise HTTPException(
            status_code=400,
            detail="Event not deleted, unable to delete from calendar",
        )


@app.put("/update_event/{event_id}")
def update_event(event_id: str, event: Event) -> dict:
    return calendar_handler.update_event_by_id(
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
    run("cal_sync_api:app", host="0.0.0.0", port=8000, log_level="info")
