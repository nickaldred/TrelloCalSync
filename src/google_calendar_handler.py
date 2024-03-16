"""This module handles requests to the Google Calendar API."""

from typing import Optional
from datetime import datetime, timedelta
from os.path import exists
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from calendar_handler import CalendarHandler
from googleapiclient.http import BatchHttpRequest


class GoogleCalendarHandler(CalendarHandler):
    """Handles requests to the Google Calendar API

    Args:
        scopes (list): The scopes to request access to.
        token_file_path (str): The path to the file to store the
        token in.
        service_account_file_path (str): The path to the service
        account file.
    """

    def __init__(
        self,
        scopes: list,
        token_file_path: str,
        service_account_file_path: str,
    ):
        creds: None | Credentials = None

        if exists(token_file_path):
            creds = Credentials.from_authorized_user_file(
                token_file_path,
                scopes,
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    service_account_file_path, scopes
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(token_file_path, "w") as token:
                token.write(creds.to_json())

        self._service = build("calendar", "v3", credentials=creds)

    def add_event(
        self,
        summary: str,
        description: str,
        start_datetime: datetime,
        end_datetime: datetime,
        location: Optional[str] = None,
        calendar_id: Optional[str] = "primary",
    ) -> Optional[str]:
        """Add an event to the calendar.

        Adds an event to the calendar with the given summary,
        description, start and end times, and location.

        Args:
            summary (str): The summary of the event.
            description (str): The description of the event.
            start_datetime (datetime): The start time of the event.
            end_datetime (datetime): The end time of the event.
            location (str): The location of the event.
            calendar_id (str): The ID of the calendar to add the
            event to.

        Returns:
            str: The ID of the event that was added.
        """

        event_to_add: dict = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_datetime.isoformat(),
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": end_datetime.isoformat(),
                "timeZone": "Europe/London",
            },
        }

        added_event = (
            self._service.events()
            .insert(
                calendarId=calendar_id,
                body=event_to_add,
            )
            .execute()
        )
        event_id: str = added_event.get("id")
        return event_id

    def get_event_by_id(
        self,
        event_id: str,
        calendar_id: str = "primary",
    ) -> dict:
        """Get an event by its ID.

        Args:
            event_id (str): The ID of the event to retrieve.
            calendar_id (str): The ID of the calendar to retrieve the
            event from.
            calendar_id (str): The ID of the calendar to retrieve the
            event from.

        Returns:
            dict: The event details.
        """

        try:
            event: dict = (
                self._service.events()
                .get(calendarId=calendar_id, eventId=event_id)
                .execute()
            )
            return event

        except HttpError as e:
            print(f"An error occurred: {e}")
            return {}

    def delete_event_by_id(
        self,
        event_id: str,
        calendar_id: str = "primary",
    ) -> dict:
        """Delete an event by its ID.

        Args:
            event_id (str): The ID of the event to delete.
            calendar_id (str): The ID of the calendar to delete the
            event from.

        Returns:
            dict: The event details.
        """

        try:
            self._service.events().delete(
                calendarId=calendar_id, eventId=event_id
            ).execute()
            return {"status": "Event deleted successfully"}

        except HttpError as e:
            print(f"An error occurred: {e}")
            return {}

    def update_event_color(
        self,
        event_id,
        color_id,
        calendar_id="primary",
    ) -> dict:
        """Update the color of an event.

        Args:
            event_id (str): The ID of the event to update.
            color_id (str): The ID of the color to use.
        """
        try:
            event: dict = (
                self._service.events()
                .get(calendarId=calendar_id, eventId=event_id)
                .execute()
            )
            event["colorId"] = color_id
            updated_event: dict = (
                self._service.events()
                .update(calendarId=calendar_id, eventId=event_id, body=event)
                .execute()
            )

            return updated_event

        except HttpError as e:
            print(f"An error occurred: {e}")
            return {}

    def get_todays_events(self, calendar_id: str = "primary") -> list:
        """Get today's events from the calendar.

        Args:
            calendar_id (str): The ID of the calendar to retrieve
            events from.

        Returns:
            list: A list of events for today.
        """
        now: str = datetime.utcnow().isoformat() + "Z"
        tomorrow: str = (
            datetime.utcnow() + timedelta(days=1)
        ).isoformat() + "Z"

        events_result: dict = (
            self._service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=tomorrow,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])

    def get_events_by_ids(self, event_ids: list, calendar_id: str = "primary") -> list:
        """Get events by their IDs.

        Args:
            event_ids (list[str]): The IDs of the events to retrieve.
            calendar_id (str): The ID of the calendar to retrieve the

        Returns:
            list[dict]: The event details.
        """

        def callback(request_id, response, exception):
            if exception is not None:
                print(f"An error occurred: {exception}")
            else:
                calendar_events.append(response)

        calendar_events: list = []
        batch = self._service.new_batch_http_request(callback=callback)
        for event_id in event_ids:
            batch.add(
                self._service.events().get(
                    calendarId=calendar_id, eventId=event_id
                )
            )
        batch.execute()
        return calendar_events


# # Example usage
# calendar_api = GoogleCalendarHandler()

# # Add an event
# summary = "Important Meeting"
# description = "Discuss project roadmap"
# start_time = datetime.datetime(2024, 2, 29, 10, 0, 0)
# end_time = datetime.datetime(2024, 2, 29, 11, 30, 0)
# # event_id = calendar_api.add_event(summary, description, start_time, end_time)

# print(calendar_api.get_todays_events())

# calendar_api.update_event_color("0aj2luk39siehndnj0n3pl0dif", 2)

# # calendar_api.delete_event_by_id("2e5usct0g52kng5ao3m0et08cf")
