from typing import Optional
from datetime import datetime
import os.path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from calendar_handler import CalendarHandler

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "credentials.json"  # Replace with your credentials file


class GoogleCalendarHandler(CalendarHandler):
    """Handles requests to the Google Calendar API"""

    def __init__(self):
        creds: None | Credentials = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES,
            )

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open("token.json", "w") as token:
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
    ) -> str:
        """Add an event to the calendar.

        Adds an event to the calendar with the given summary, description,
        start and end times, and location.

        Args:
        """
        event: dict = {
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

        event: dict = (
            self._service.events()
            .insert(
                calendarId=calendar_id,
                body=event,
            )
            .execute()
        )
        event_id: str = event.get("id")
        return event_id

    def get_event_by_id(self, event_id: str) -> dict:
        """Get an event by its ID.

        Args:
            event_id (str): The ID of the event to retrieve.

        Returns:
            dict: The event details.
        """
        try:
            event: dict = (
                self._service.events()
                .get(calendarId="primary", eventId=event_id)
                .execute()
            )
            return event
        except HttpError as e:
            print(f"An error occurred: {e}")
            return None

    def delete_event_by_id(self, event_id):
        """Delete an event by its ID.

        Args:
            event_id (str): The ID of the event to delete.
        """
        try:
            self._service.events().delete(
                calendarId="primary", eventId=event_id
            ).execute()
            print(f"Event with ID {event_id} has been deleted.")
        except HttpError as e:
            print(f"An error occurred: {e}")

    def update_event_color(self, event_id, color_id):
        """Update the color of an event.

        Args:
            event_id (str): The ID of the event to update.
            color_id (str): The ID of the color to use.
        """
        try:
            event = (
                self._service.events()
                .get(calendarId="primary", eventId=event_id)
                .execute()
            )
            event["colorId"] = color_id
            updated_event = (
                self._service.events()
                .update(calendarId="primary", eventId=event_id, body=event)
                .execute()
            )
            print(f"Event color updated to {color_id}.")
            return updated_event
        except HttpError as e:
            print(f"An error occurred: {e}")
            return None

    def get_todays_events(self) -> list:
        """Get today's events from the calendar.

        Returns:
            list: A list of events for today.
        """
        now = datetime.datetime.utcnow().isoformat() + "Z"
        tomorrow = (
            datetime.datetime.utcnow() + datetime.timedelta(days=1)
        ).isoformat() + "Z"

        events_result = (
            self._service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                timeMax=tomorrow,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        return events_result.get("items", [])


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
