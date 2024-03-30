"""Main file for the calendar sync program."""

from multiprocessing import Process
from os import environ
import cal_sync_api
from dotenv import load_dotenv
from factorys import calendar_handler_factory, db_handler_factory
from google_calendar_handler import GoogleCalendarHandler
from mongodb_handler import MongoDbHandler
from sync_processor import SyncProcessor

load_dotenv("./.env")


class CalendarSync:
    """Main class for the calendar sync program."""

    def __init__(self):
        self._calendar_handler: GoogleCalendarHandler = (
            calendar_handler_factory(environ["CALENDAR_TYPE"])
        )

        self._test_db_handler: MongoDbHandler = db_handler_factory(
            environ["DB_TYPE"]
        )
        self._sync_processor: SyncProcessor = SyncProcessor(
            self._calendar_handler, self._test_db_handler
        )

    def main(self):
        """Runs all the processes of the program."""

        process_1: Process = Process(
            target=cal_sync_api.run,
            args=("cal_sync_api:APP",),
            kwargs={
                "host": environ["API_HOST"],
                "port": int(environ["API_PORT"]),
                "log_level": environ["LOG_LEVEL"].lower(),
            },
        )

        process_2: Process = Process(
            target=self._sync_processor.sync,
            args=(int(environ["SYNC_INTERVAL"]),),
        )

        # Start processes
        process_1.start()
        process_2.start()

        # Wait for processes to finish
        process_1.join()
        process_2.join()


if __name__ == "__main__":
    calendar_sync: CalendarSync = CalendarSync()
    calendar_sync.main()
