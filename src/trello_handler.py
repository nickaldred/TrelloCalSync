"""
This module contains the TrelloHandler class, which is responsible
for all interactions with the Trello API.
"""

from json import dumps as json_dumps
import trello
from board_handler import BoardHandler
from data_models import Board, BoardCard, BoardList
from trello import Board as TrelloBoard
from trello import Card as TrelloCard
from trello import List as TrelloList
from trello import TrelloClient


def patched_fetch_json(
    self,
    uri_path,
    http_method="GET",
    headers=None,
    query_params=None,
    post_args=None,
    files=None,
):
    """Fetch some JSON from Trello"""

    # explicit values here to avoid mutable default values
    if headers is None:
        headers = {}
    if query_params is None:
        query_params = {}
    if post_args is None:
        post_args = {}

    # if files specified, we don't want any data
    data = None
    if files is None and post_args != {}:
        data = json_dumps(post_args)

    # set content type and accept headers to handle JSON
    if http_method in ("POST", "PUT", "DELETE") and not files:
        headers["Content-Type"] = "application/json; charset=utf-8"

    headers["Accept"] = "application/json"

    # construct the full URL without query parameters
    if uri_path[0] == "/":
        uri_path = uri_path[1:]
    url = "https://api.trello.com/1/%s" % uri_path

    if self.oauth is None:
        query_params["key"] = self.api_key
        query_params["token"] = self.api_secret

    # perform the HTTP requests, if possible uses OAuth authentication
    response = self.http_service.request(
        http_method,
        url,
        params=query_params,
        headers=headers,
        data=data,
        auth=self.oauth,
        files=files,
        proxies=self.proxies,
    )

    if response.status_code == 401:
        raise trello.Unauthorized("%s at %s" % (response.text, url), response)
    if response.status_code != 200:
        raise trello.ResourceUnavailable(
            "%s at %s" % (response.text, url), response
        )

    return response.json()


trello.TrelloClient.fetch_json = patched_fetch_json


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
