"""
This module contains the TrelloHandler class, which is responsible
for all interactions with the Trello API.
"""

from trello import Card, TrelloClient, Board, List as TrelloList
from board_handler import BoardHandler


class TrelloHandler(BoardHandler):
    """Handles all interactions with the Trello API."""

    def __init__(self, api_key: str, api_secret: str, token: str):
        self.client = TrelloClient(
            api_key=api_key,
            api_secret=api_secret,
            token=token,
        )

    def get_cards_in_list(self, board_id: str, list_id: str) -> list[Card]:
        """Gets all cards within a specific list (column) on a board.

        Args:
            board_id: The ID of the board containing the list.
            list_id: The ID of the list to get cards from.

        Returns:
            A list of all cards in the list.
        """

        board: Board = self.client.get_board(board_id)
        target_list: TrelloList = board.get_list(list_id)
        return target_list.list_cards()

    def get_all_boards(self) -> list[Board]:
        """Gets the IDs of all boards accessible to the user.

        Returns:
            A list of all boards accessible to the user.
        """

        return self.client.list_boards()

    def get_all_lists(self, board_id: str) -> list[TrelloList]:
        """Gets the IDs of all lists on a specific board.

        Args:
            board_id: The ID of the board to get lists from.

        Returns:
            A list of all lists on the board.
        """

        board: Board = self.client.get_board(board_id)
        return board.list_lists()

    def update_card_list(self, card_id: str, new_list_id: str) -> Card:
        """Moves a card to a different list (column).

        Args:
            card_id: The ID of the card to move.
            new_list_id: The ID of the list to move the card to.

        Returns:
            The updated card.
        """

        card: Card = self.client.get_card(card_id)
        new_list: TrelloList = self.client.get_list(new_list_id)
        card.change_list(new_list.id)
        return card
