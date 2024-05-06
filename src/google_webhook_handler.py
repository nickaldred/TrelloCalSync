"""Module to handle Google Calendar webhooks."""

from json import JSONDecodeError
from json import loads as json_loads
from os.path import exists
from uuid import uuid4
from calendar_webhook_handler import CalendarWebhookHandler
from dotenv import load_dotenv
from exceptions import CalendarWebhookError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv("./.env")


class GoogleWebhookHandler(CalendarWebhookHandler):
    """Class to handle Google Calendar webhooks."""

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
            with open(token_file_path, "w", encoding="utf-8") as token:
                token.write(creds.to_json())

        self._service = build("calendar", "v3", credentials=creds)

    def create_webhook(
        self, webhook_url: str, calendar_id: str = "primary"
    ) -> dict:
        """Create a webhook for the Google Calendar.

        Args:
            webhook_url (str): The URL to send the webhook to.
            calendar_id (str): The ID of the calendar to add the webhook to.

        Returns:
            dict: The response from the API.

        Raises:
            CalendarWebhookError: If the webhook could not be created.
        """

        channel: dict = {
            "id": str(uuid4()),
            "type": "web_hook",
            "address": webhook_url,
        }

        try:
            response: str = (
                self._service.events()
                .watch(
                    calendarId=calendar_id,
                    body=channel,
                )
                .execute()
            )
            print("Webhook added successfully!")

            return json_loads(response)

        except (HttpError, JSONDecodeError) as error:
            print(f"Failed to add webhook: {error}")
            raise CalendarWebhookError(
                f"Failed to add webhook: {error}"
            ) from error

    def delete_webhook(self, channel_id: str, resource_id: str) -> bool:
        """Delete a webhook for the Google Calendar.

        Args:
            channel_id (str): The ID of the channel.
            resource_id (str): The ID of the resource.

        Returns:
            bool: True if the webhook was deleted successfully.

        Raises:
            CalendarWebhookError: If the webhook could not be deleted.
        """
        try:
            self._service.channels().stop(
                body={
                    "id": channel_id,
                    "resourceId": resource_id,
                }
            ).execute()
            print("Webhook deleted successfully!")
            return True

        except HttpError as e:
            print(f"Failed to delete webhook: {e}")
            raise CalendarWebhookError(f"Failed to delete webhook: {e}") from e
