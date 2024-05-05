"""Module for handling Trello webhook interactions."""

from typing import Dict
from requests import post, delete, Response
from exceptions import TrelloWebhookError


class TrelloWebhookHandler:
    """Handles all interactions with the Trello webhook API."""

    def __init__(self, api_key: str, token: str):
        self.api_key: str = api_key
        self.token: str = token

    def add_webhook(
        self,
        description: str,
        callback_url: str,
        model_id: str,
    ) -> str:
        """
        Add a webhook to Trello.

        Args:
            description (str): The description of the webhook.
            callback_url (str): The URL to receive webhook
            notifications.
            model_id (str): The ID of the Trello model to attach
            the webhook to.

        Returns:
            str: The response text from the API.

        """
        url = f"https://api.trello.com/1/tokens/{self.token}/webhooks/"
        payload: dict[str, str] = {
            "key": self.api_key,
            "description": description,
            "callbackURL": callback_url,
            "idModel": model_id,
        }
        response = post(url, json=payload, timeout=30)
        return response

    def delete_webhook(
        self,
        webhook_id: str,
    ) -> Response:
        """
        Delete a webhook from Trello.

        Args:
            webhook_id (str): The ID of the webhook to delete.

        Returns:
            requests.Response: The response from the API.

        """
        url: str = (
            "https://api.trello.com/1/webhooks/"
            f"{webhook_id}?key={self.api_key}&token={self.token}"
        )
        headers: dict = {"Content-Type": "application/json"}
        response = delete(url, headers=headers, timeout=30)

        if response.status_code != 200:
            raise TrelloWebhookError(
                f"Failed to delete webhook: {response.text}"
            )

        return response
