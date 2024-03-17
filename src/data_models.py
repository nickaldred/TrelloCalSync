"""Data models for the program"""

from dataclasses import dataclass


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
