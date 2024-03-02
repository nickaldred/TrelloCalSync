"""Interface for board API handlers."""

from abc import ABC, abstractmethod
from typing import List
from data_models import BoardCard, BoardList, Board


class BoardHandler(ABC):
    """Abstract base class for API handlers."""

    @abstractmethod
    def __init__(self, api_key: str, api_secret: str, token: str):
        """
        Initialize the AbstractHandler.

        Args:
            api_key (str): The API key.
            api_secret (str): The API secret.
            token (str): The authentication token.
        """

    @abstractmethod
    def get_cards_in_list(self, board_id: str, list_id: str) -> List[BoardCard]:
        """
        Get the cards in a specific list.

        Args:
            board_id (str): The ID of the board.
            list_id (str): The ID of the list.

        Returns:
            List: A list of cards in the specified list.
        """

    @abstractmethod
    def get_all_boards(self) -> List[Board]:
        """
        Get all the boards.

        Returns:
            List: A list of all the boards.
        """

    @abstractmethod
    def get_all_lists(self, board_id: str) -> List[BoardList]:
        """
        Get all the lists in a board.

        Args:
            board_id (str): The ID of the board.

        Returns:
            List: A list of all the lists in the specified board.
        """

    @abstractmethod
    def update_card_list(self, card_id: str, new_list_id: str) -> BoardCard:
        """
        Update the list of a card.

        Args:
            card_id (str): The ID of the card.
            new_list_id (str): The ID of the new list.
        """
