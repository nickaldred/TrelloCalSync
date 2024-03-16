"""Package for exceptions."""


class FactoryError(Exception):
    """The base class for factory errors."""

    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)