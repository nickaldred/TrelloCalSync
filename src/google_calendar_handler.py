"""This module handles requests to the Google Calendar API."""

from datetime import datetime, timedelta
from os.path import exists
from typing import Optional
from calendar_handler import CalendarHandler
from data_models import Event
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
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
        event: Event,
    ) -> Optional[str]:
        """Add an event to the calendar.

        Adds an event to the calendar with the given title,
        description, start and end times, color id, and location.

        Args:
            event (Event): The event to add.

        Returns:
            str: The ID of the event that was added.
        """

        event_to_add: dict = {
            "summary": event.title,
            "location": event.location,
            "description": event.description,
            "colorId": event.colour_id,
            "start": {
                "dateTime": event.start_datetime,
                "timeZone": event.timezone,
            },
            "end": {
                "dateTime": event.end_datetime,
                "timeZone": event.timezone,
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

    def get_events_by_ids(
        self, event_ids: list, calendar_id: str = "primary"
    ) -> dict:
        """Get events by their IDs.

        Args:
            event_ids (list[str]): The IDs of the events to retrieve.
            calendar_id (str): The ID of the calendar to retrieve the

        Returns:
            dict: A dictionary of events, with the event IDs as keys.
        """

        def callback(request_id, response, exception):
            if exception is not None:
                print(f"An error occurred: {exception}")

            else:
                event_color_id = response.get("colorId", "Not specified")
                response["colorId"] = event_color_id
                calendar_events[request_id] = response

        calendar_events: dict = {}
        batch: BatchHttpRequest = self._service.new_batch_http_request(
            callback=callback
        )
        for event_id in event_ids:
            batch.add(
                self._service.events().get(
                    calendarId=calendar_id, eventId=event_id
                ),
                request_id=event_id,
            )
        batch.execute()
        return calendar_events
