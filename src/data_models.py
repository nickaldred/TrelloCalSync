"""Data models for the program"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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
