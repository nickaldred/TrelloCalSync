"""Module for handling webhook interactions with boards."""

from abc import ABC, abstractmethod


class BoardWebhookHandler(ABC):
    """Abstract base class for handling webhook interactions with Trello."""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def create_webhook(
        self, description: str, callback_url: str, model_id: str
    ) -> dict:
        """
        Create a webhook for the board.
        """

    @abstractmethod
    def delete_webhook(self, webhook_id: str) -> bool:
        """
        Delete a webhook from Trello.
        """
