"""
This module contains the TrelloHandler class, which is responsible
for all interactions with the Trello API.
"""

from trello import (
    Card as TrelloCard,
    TrelloClient,
    Board as TrelloBoard,
    List as TrelloList,
)
from board_handler import BoardHandler
from data_models import BoardCard, BoardList, Board


class TrelloHandler(BoardHandler):
    """Handles all interactions with the Trello API.

    Args:
        api_key: The API key for the Trello API.
        api_secret: The API secret for the Trello API.
        token: The token for the Trello API.
    """

    def __init__(self, api_key: str, api_secret: str, token: str):
        self.client = TrelloClient(
            api_key=api_key,
            api_secret=api_secret,
            token=token,
        )

    def get_cards_in_list(
        self,
        board_id: str,
        list_id: str,
    ) -> list[BoardCard]:
        """Gets all cards within a specific list (column) on a board.

        Args:
            board_id: The ID of the board containing the list.
            list_id: The ID of the list to get cards from.

        Returns:
            A list of all cards in the list.
        """

        board: TrelloBoard = self.client.get_board(board_id)
        target_list: TrelloList = board.get_list(list_id)
        trello_cards = target_list.list_cards()
        return [
            BoardCard(
                id=card.id,
                name=card.name,
                desc=card.desc,
                list_id=list_id,
            )
            for card in trello_cards
        ]

    def get_all_boards(self) -> list[Board]:
        """Gets the IDs of all boards accessible to the user.

        Returns:
            A list of all boards accessible to the user.
        """
        trello_boards = self.client.list_boards()
        return [
            Board(
                id=board.id,
                name=board.name,
                closed=board.closed,
            )
            for board in trello_boards
        ]

    def get_all_lists(self, board_id: str) -> list[BoardList]:
        """Gets the IDs of all lists on a specific board.

        Args:
            board_id: The ID of the board to get lists from.

        Returns:
            A list of all lists on the board.
        """

        board: TrelloBoard = self.client.get_board(board_id)
        trello_lists = board.list_lists()
        return [
            BoardList(
                id=list.id,
                name=list.name,
                closed=list.closed,
                board_id=board_id,
            )
            for list in trello_lists
        ]

    def update_card_list(self, card_id: str, new_list_id: str) -> BoardCard:
        """Moves a card to a different list (column).

        Args:
            card_id: The ID of the card to move.
            new_list_id: The ID of the list to move the card to.

        Returns:
            The updated card.
        """
        card: TrelloCard = self.client.get_card(card_id)
        new_list: TrelloList = self.client.get_list(new_list_id)
        card.change_list(new_list.id)
        return BoardCard(
            id=card.id, name=card.name, desc=card.desc, list_id=new_list.id
        )

    def get_card(self, card_id: str) -> BoardCard:
        """Gets a card by its ID.

        Args:
            card_id: The ID of the card to get.

        Returns:
            The card with the given ID.
        """
        card: TrelloCard = self.client.get_card(card_id)
        return BoardCard(
            id=card.id,
            name=card.name,
            desc=card.desc,
            list_id=card.idList,
        )