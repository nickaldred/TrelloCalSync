"""Main file for the calendar sync program."""

from os import environ
from dotenv import load_dotenv
from multiprocessing import Process
import cal_sync_api

load_dotenv("./.env")


class CalendarSync:
    """Main class for the calendar sync program."""

    def __init__(self):
        pass

    def main(self):
        """Runs all the processes of the program."""

        process_1 = Process(
            target=cal_sync_api.run,
            args=("cal_sync_api:APP",),
            kwargs={
                "host": environ["API_HOST"],
                "port": int(environ["API_PORT"]),
                "log_level": environ["LOG_LEVEL"].lower(),
            },
        )
        # p2 = Process(target=sync_calendar2)

        # Start processes
        process_1.start()
        # p2.start()

        # Wait for processes to finish
        process_1.join()
        # p2.join()


if __name__ == "__main__":
    calendar_sync: CalendarSync = CalendarSync()
    calendar_sync.main()
