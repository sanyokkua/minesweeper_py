"""_summary_"""
import enum


class ControllerActionMarkers(enum.Enum):
    """_summary_

    Args:
        enum (_type_): _description_
    """
    NEW_GAME: int = 0
    RESET_GAME: int = 1
    CELL_FLAGGED: int = 2
    CELL_OPENED: int = 3
