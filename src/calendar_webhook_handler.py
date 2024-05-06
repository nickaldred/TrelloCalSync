"""Module to handle Calendar webhooks."""

from abc import ABC, abstractmethod


class CalendarWebhookHandler(ABC):
    """Abstract base class to handle Calendar webhooks."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create_webhook(
        self, webhook_url: str, calendar_id: str = "primary"
    ) -> dict:
        """Create a webhook for the Calendar.

        Args:
            webhook_url (str): The URL to send the webhook to.
            calendar_id (str): The ID of the calendar to add the webhook to.

        Returns:
            dict: The response from the API.

        Raises:
            CalendarWebhookError: If the webhook could not be created.
        """

    @abstractmethod
    def delete_webhook(self, channel_id: str, resource_id: str) -> bool:
        """Delete a webhook for the Calendar.

        Args:
            channel_id (str): The ID of the channel.
            resource_id (str): The ID of the resource.

        Returns:
            bool: True if the webhook was deleted successfully.

        Raises:
            CalendarWebhookError: If the webhook could not be deleted.
        """
