"""Module contains IncorrectCoordinatesException class."""


class IncorrectCoordinatesException(Exception):
    """Incorrect coordinate exception used by game logic."""

    def __init__(self, message: str) -> None:
        """Initialize default exception with a message.

        Args:
            message (str): Message description of the problem.
        """
        Exception.__init__(self, message)
