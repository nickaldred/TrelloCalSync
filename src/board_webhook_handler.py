"""Module for handling webhook interactions with boards."""

from abc import ABC, abstractmethod


class BoardWebhookHandler(ABC):
    """Abstract base class for handling webhook interactions with Trello."""

    def __init__(self, api_key: str, token: str):
        self.api_key: str = api_key
        self.token: str = token

    @abstractmethod
    def add_webhook(
        self, description: str, callback_url: str, model_id: str
    ) -> dict:
        """
        Add a webhook to Trello.
        """

    @abstractmethod
    def delete_webhook(self, webhook_id: str) -> bool:
        """
        Delete a webhook from Trello.
        """
