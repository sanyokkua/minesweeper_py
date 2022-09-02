import enum


class ControllerActionMarkers(enum.Enum):
    NEW_GAME = 0
    RESET_GAME = 1
    CELL_FLAGGED = 2
    CELL_OPENED = 3
