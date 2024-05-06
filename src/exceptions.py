"""Package for exceptions."""


class FactoryError(Exception):
    """The base class for factory errors."""

    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)


class SyncError(Exception):
    """The base class for sync errors."""

    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)


class TrelloWebhookError(Exception):
    """The base class for Trello webhook errors."""

    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)
