"""Module for handling Trello webhook interactions."""

from json import JSONDecodeError
from json import loads as json_loads
from exceptions import TrelloWebhookError
from requests import RequestException, Response, delete, post


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
    ) -> dict:
        """
        Add a webhook to Trello.

        Args:
            description (str): The description of the webhook.
            callback_url (str): The URL to receive webhook notifications.
            model_id (str): The ID of the Trello model to attach the
            webhook to.

        Example response::
        {
            'id': '663752ec6367f387f418e99b',
            'description': '65f6b9c672c8590dca310e37',
            'idModel': '60f6b9c672c8590dca310e37',
            'callbackURL': 'https://desktop-v4sacft.tail67257.ts.net/webhook/',
            'active': True,
            'consecutiveFailures': 0,
            'firstConsecutiveFailDate': None
        }

        Returns:
            dict: The response from the API.
        """

        url: str = f"https://api.trello.com/1/tokens/{self.token}/webhooks/"
        payload: dict[str, str] = {
            "key": self.api_key,
            "description": description,
            "callbackURL": callback_url,
            "idModel": model_id,
        }

        try:
            response: Response = post(url, json=payload, timeout=30)

            if response.status_code != 200:
                raise TrelloWebhookError(
                    f"Failed to add webhook: {response.text}"
                )

            return json_loads(response.text)

        except (RequestException, JSONDecodeError) as error:
            print(f"Error adding webhook: {error}")
            raise TrelloWebhookError(f"Failed to add webhook: {error}")

    def delete_webhook(
        self,
        webhook_id: str,
    ) -> bool:
        """
        Delete a webhook from Trello.

        Args:
            webhook_id (str): The ID of the webhook to delete.

        Returns:
            bool: True if the webhook was deleted successfully.

        """
        url: str = (
            "https://api.trello.com/1/webhooks/"
            f"{webhook_id}?key={self.api_key}&token={self.token}"
        )
        headers: dict = {"Content-Type": "application/json"}

        try:
            response: Response = delete(url, headers=headers, timeout=30)

            if response.status_code != 200:
                print(f"Error deleting webhook: {response.text}")
                raise TrelloWebhookError(
                    f"Failed to delete webhook: {response.text}"
                )

            return True

        except RequestException as error:
            print(f"Error deleting webhook: {error}")
            raise TrelloWebhookError(f"Failed to delete webhook: {error}")
