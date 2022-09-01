"""Representation of the Controller API functionality."""
import logging
from typing import Callable

from minesweeper_core.api.dtos import GameInformation
from minesweeper_core.constants.default_configurations import BEGINNER
from minesweeper_core.data.field_configuration import Configuration
from minesweeper_core.logic.game_logic import GameLogic

log: logging.Logger = logging.getLogger(__name__)


class MinesweeperController:
    """Controller of the game."""

    def __init__(self, on_game_status_update_callback: Callable[[GameInformation], None] = None) -> None:
        log.debug('Init controller')
        self._game_instance: GameLogic | None = None
        self._last_config: Configuration = BEGINNER
        self._on_game_status_update_callback = on_game_status_update_callback
        log.debug('Init controller, game_instance: %s, config: %s',
                  self._game_instance,
                  self._last_config)

    def start_new_game(self, config: Configuration) -> None:
        log.debug('start_new_game, with config: %s', config)
        self._last_config = config
        self._game_instance = GameLogic(self._last_config)
        if self._on_game_status_update_callback:
            self._on_game_status_update_callback(self.get_game_info())

    def reset_game(self) -> None:
        log.debug('reset_game, with config: %s', self._last_config)
        self._game_instance = GameLogic(self._last_config)
        if self._on_game_status_update_callback:
            self._on_game_status_update_callback(self.get_game_info())

    def open_cell(self, row: int, column: int) -> None:
        log.debug('open_cell, with row: %d, col: %d', row, column)
        if self._game_instance:
            self._game_instance.open_cell(row, column)
        if self._on_game_status_update_callback:
            self._on_game_status_update_callback(self.get_game_info())

    def flag_cell(self, row: int, column: int) -> None:
        log.debug('flag_cell, with row: %d, col: %d', row, column)
        if self._game_instance:
            self._game_instance.flag_cell(row, column)
        if self._on_game_status_update_callback:
            self._on_game_status_update_callback(self.get_game_info())

    def get_game_info(self) -> GameInformation | None:
        log.debug('get_game_info')
        if self._game_instance:
            info = GameInformation(
                number_of_rows=self._game_instance.rows,
                number_of_columns=self._game_instance.columns,
                number_of_mines=self._game_instance.number_of_mines,
                number_of_flags_left=self._game_instance.number_of_flags,
                game_field=self._game_instance.field,
                is_finished=self._game_instance.is_game_finished,
                is_player_win=self._game_instance.is_player_win
            )
            log.debug('get_game_info, info: %s', info)
            return info
        else:
            log.debug('get_game_info, info: None')
            return None
