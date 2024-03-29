"""Syncs the board and calendar."""

from google_calendar_handler import GoogleCalendarHandler
from mongodb_handler import MongoDbHandler
from trello_handler import TrelloHandler
from exceptions import SyncError
import factorys


class SyncProcessor:
    """Syncs the board and calendar"""

    def __init__(
        self,
        calendar_handler: GoogleCalendarHandler,
        db_handler: MongoDbHandler,
    ):
        self.calendar_handler: GoogleCalendarHandler = calendar_handler
        self.db_handler: MongoDbHandler = db_handler

    def sync(
        self,
    ):
        """Syncs the calendar with the board events"""

        events: dict = self.db_handler.get_all_documents("calendar_events")

        if not events:
            raise SyncError("No events found")

        calendar_events: dict = self.get_calendar_events(events)
        print(calendar_events)

        if not calendar_events:
            raise SyncError("No events found")

        events_to_sync: list = self.compare_events(calendar_events, events)

    def get_calendar_events(self, events: list[dict]) -> dict:
        """Gets the events from the calendar.

        Returns:
            dict: The calendar events.
        """

        event_ids: list = [event["event_id"] for event in events]

        calendar_events: dict = self.calendar_handler.get_events_by_ids(
            event_ids
        )
        return calendar_events

    def compare_events(
        self, calendar_events: dict, events: list[dict]
    ) -> list:
        """Compares the events to check if they are in sync."""

        events_to_sync: list = []

        return events_to_sync

    def sync_up_events(self):
        """Syncs up the out of sync board and calendar events."""


calendar_handler = factorys.calendar_handler_factory("google")
db_handler = factorys.db_handler_factory("mongo")


test = SyncProcessor(calendar_handler, db_handler)
test.sync()
