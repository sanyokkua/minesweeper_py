"""_summary_"""
from dataclasses import dataclass

from minesweeper_core.api.controller_action_markers import \
    ControllerActionMarkers
from minesweeper_core.data.cell import Cell


@dataclass(repr=True, frozen=True)
class GameInformation:
    """_summary_"""
    number_of_rows: int
    number_of_columns: int
    number_of_mines: int
    number_of_flags_left: int
    game_field: dict[tuple[int, int], Cell]
    is_finished: bool
    is_player_win: bool
    controller_action: ControllerActionMarkers
