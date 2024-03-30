"""
This module contains the interface for calendar handlers. It is used to
define the methods that should be implemented by concrete calendar handler
classes.
"""

from abc import ABC, abstractmethod
from data_models import Event


class CalendarHandler(ABC):
    """Interface for calendar handlers"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_event(
        self,
        event: Event,
    ):
        """Adds an event to the calendar"""

    @abstractmethod
    def get_event_by_id(self, event_id: str, calendar_id: str):
        """Gets an event from the calendar by its ID"""

    @abstractmethod
    def delete_event_by_id(self, event_id: str, calendar_id: str):
        """Deletes an event from the calendar by its ID"""

    @abstractmethod
    def update_event_color(
        self,
        event_id: str,
        color_id: str,
        calendar_id: str,
    ):
        """Updates the color of an event in the calendar"""

    @abstractmethod
    def get_todays_events(self, calendar_id: str) -> list:
        """Gets today's events from the calendar"""
