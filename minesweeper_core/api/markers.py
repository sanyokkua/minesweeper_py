"""Module contains ControllerActions class."""
import enum


class ControllerActions(enum.Enum):
    """Markers for GameInformation.

    Args:
        enum (_type_): Defines Enum Class
    """

    NEW_GAME: int = 0
    RESET_GAME: int = 1
    CELL_FLAGGED: int = 2
    CELL_OPENED: int = 3
