"""Syncs the board and calendar."""

from google_calendar_handler import GoogleCalendarHandler
from mongodb_handler import MongoDbHandler
from trello_handler import TrelloHandler
from exceptions import SyncError


class SyncProcessor:
    """Syncs the board and calendar"""

    def __init__(
        self,
        calendar_handler: GoogleCalendarHandler,
        db_handler: MongoDbHandler,
        board_handler: TrelloHandler,
    ):
        self.calendar_handler: GoogleCalendarHandler = calendar_handler
        self.db_handler: MongoDbHandler = db_handler
        self.board_handler: TrelloHandler = board_handler

    def sync(
        self,
    ):
        """Syncs the calendar with the board events"""

        events = self.db_handler.get_collection("calendar_events")

        if not events:
            raise SyncError
        
        

        # get board events
        # get calendar events
        # check they match
        # make any adjustments

    def get_board_events(self):
        """Gets the events from the board."""

    def get_calendar_events(self):
        """Gets the events from the calendar."""

    def compare_events(self):
        """Compares the events to check if they are in sync."""

    def sync_up_events(self):
        """Syncs up the out of sync board and calendar events."""



