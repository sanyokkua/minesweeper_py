"""Module contains ControllerActions class."""
import enum


class ControllerActions(enum.Enum):
    """Markers for GameInformation.

    Args:
        enum.Enum (_type_): Defines Enum Class
    """

    NEW_GAME = 0
    RESET_GAME = 1
    CELL_FLAGGED = 2
    CELL_OPENED = 3
