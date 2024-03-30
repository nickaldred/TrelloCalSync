"""Data models for the program"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CalendarEvent(BaseModel):
    """Calendar event model."""

    summary: str
    location: Optional[str]
    description: str
    colorId: Optional[int]
    start: dict
    end: dict


class Event(BaseModel):
    """The event model."""

    title: str
    description: str
    start_datetime: str
    end_datetime: str
    location: Optional[str] = None
    calendar_id: str = "primary"
    card_id: str
    board_id: str
    current_status: str = "TO_DO"
    colour_id: Optional[int] = None
    event_id: Optional[str] = None
    timezone: str = "Europe/London"
    created_at: str = datetime.now().isoformat()

    def get_calendar_event(self) -> CalendarEvent:
        """Return the event in the required format.

        Returns:
            CalendarEvent: The event in the required format.
        """

        return CalendarEvent(
            summary=self.title,
            location=self.location,
            description=self.description,
            colorId=self.colour_id,
            start={
                "dateTime": self.start_datetime,
                "timeZone": self.timezone,
            },
            end={
                "dateTime": self.end_datetime,
                "timeZone": self.timezone,
            },
        )


@dataclass
class BoardCard:
    """Data model for a card on a board."""

    id: str
    name: str
    desc: str
    list_id: str
    board_id: str


@dataclass
class BoardList:
    """Data model for a list on a board."""

    id: str
    name: str
    closed: bool
    board_id: str


@dataclass
class Board:
    """Data model for a board."""

    id: str
    name: str
    closed: bool
