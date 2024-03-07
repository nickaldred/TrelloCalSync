from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from google_calendar_handler import GoogleCalendarHandler
from mongodb_handler import MongoDbHandler
from uvicorn import run

app = FastAPI()


def calendar_handler_factory(type_of_handler: str):
    if type_of_handler == "google":
        return GoogleCalendarHandler(
            scopes=[
                "https://www.googleapis.com/auth/calendar",
            ],
            token_file_path="token.json",
            service_account_file_path="credentials.json",
        )
    else:
        return None


def db_handler_factory(type_of_handler: str):
    if type_of_handler == "mongo":
        return MongoDbHandler(host="localhost", port=27017, db_name="cal_sync")
    else:
        return None


calendar_handler = calendar_handler_factory("google")
db_handler_factory = db_handler_factory("mongo")


class Event(BaseModel):
    summary: str
    description: str
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str] = None
    calendar_id: Optional[str] = "primary"


@app.post("/add_event")
def add_event(event: Event):
    return calendar_handler.add_event(
        event.summary,
        event.description,
        event.start_datetime,
        event.end_datetime,
        event.location,
        event.calendar_id,
    )


@app.get("/get_event/{event_id}")
def get_event(event_id: str, calendar_id: str = "primary"):
    return calendar_handler.get_event_by_id(event_id, calendar_id)


@app.delete("/delete_event/{event_id}")
def delete_event(event_id: str, calendar_id: str = "primary"):
    return calendar_handler.delete_event_by_id(event_id, calendar_id)


@app.put("/update_event/{event_id}")
def update_event(event_id: str, event: Event):
    return calendar_handler.update_event_by_id(
        event_id,
        event.summary,
        event.description,
        event.start_datetime,
        event.end_datetime,
        event.location,
        event.calendar_id,
    )


if __name__ == "__main__":
    run("cal_sync_api:app", host="0.0.0.0", port=8000, log_level="info")
