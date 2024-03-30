"""Syncs the board and calendar."""

from time import sleep
from config import Config, get_config
from exceptions import SyncError
from factorys import calendar_handler_factory, db_handler_factory
from google_calendar_handler import GoogleCalendarHandler
from mongodb_handler import MongoDbHandler


class SyncProcessor:
    """Syncs the board and calendar"""

    def __init__(
        self,
        calendar_handler: GoogleCalendarHandler,
        db_handler: MongoDbHandler,
    ):
        self._calendar_handler: GoogleCalendarHandler = calendar_handler
        self._db_handler: MongoDbHandler = db_handler
        self._config: Config = get_config()

    def sync(self, sync_interval: int = 60) -> None:
        """Syncs the board and calendar at regular intervals.

        Args:
            sync_interval (int): The interval in seconds between syncs.
        """

        while True:
            self.sync_events()
            sleep(sync_interval)

    def sync_events(
        self,
    ):
        """Syncs the calendar with the board events"""

        events: list = self._db_handler.get_all_documents("calendar_events")

        if not events:
            raise SyncError("No events found")

        calendar_events: dict = self.get_calendar_events(events)

        if not calendar_events:
            raise SyncError("No events found")

        events_to_sync: list = self.compare_events(calendar_events, events)

        if events_to_sync:
            self.sync_up_events(events_to_sync)

    def get_calendar_events(self, events: list[dict]) -> dict:
        """Gets the events from the calendar.

        Returns:
            dict: The calendar events.
        """

        event_ids: list = [event["event_id"] for event in events]

        calendar_events: dict = self._calendar_handler.get_events_by_ids(
            event_ids
        )
        return calendar_events

    def compare_events(
        self, calendar_events: dict, events: list[dict]
    ) -> list:
        """Compares the events to check if they are in sync.

        Args:
            calendar_events (dict): The calendar events.
            events (list[dict]): The board events.

        Returns:
            list: The events to sync.
        """

        events_to_sync: list = []

        for event in events:
            event_id: str = event["event_id"]

            if event_id not in calendar_events:
                events_to_sync.append(event)
            else:
                if not self._config.get_status_colour_id(
                    event["current_status"]
                ) == int(calendar_events[event_id]["colorId"]):
                    events_to_sync.append(event)
                    print("Event out of sync")
                else:
                    print("Event in sync")

        return events_to_sync

    def sync_up_events(self, events_to_sync: list):
        """Syncs up the out of sync board and calendar events."""


if __name__ == "__main__":

    # Test the SyncProcessor class
    test_calendar_handler: GoogleCalendarHandler = calendar_handler_factory(
        "google"
    )
    test_db_handler: MongoDbHandler = db_handler_factory("mongo")

    test_sync_processor: SyncProcessor = SyncProcessor(
        test_calendar_handler, test_db_handler
    )
    test_sync_processor.sync()
