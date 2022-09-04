"""Module contains Game Controller class."""
import logging
from typing import Callable

from minesweeper_core.api.dtos import GameInformation
from minesweeper_core.api.markers import ControllerActions
from minesweeper_core.constants.configurations import BEGINNER
from minesweeper_core.data.field_configuration import Configuration
from minesweeper_core.logic.game_logic import GameLogic

log: logging.Logger = logging.getLogger(__name__)

StatusUpdateCallback = Callable[[GameInformation], None]


class MinesweeperController:
    """Controller of the Minesweeper Game."""

    def __init__(
            self,
            on_game_status_update_callback: StatusUpdateCallback = None):
        """Initialize controller with default values.

        Args:
            on_game_status_update_callback (StatusUpdateCallback, optional):
                CallBack function that will be called on the updates of
                game state.               Defaults to None.
        """
        log.debug('Init controller')
        self._game_instance: GameLogic | None = None
        self._last_config: Configuration = BEGINNER
        self._on_game_status_update_callback = on_game_status_update_callback
        log.debug('Init controller, game_instance: %s, config: %s',
                  self._game_instance,
                  self._last_config)

    def start_new_game(self, config: Configuration) -> None:
        """Start new game session.

        Creates a new instance of the GameLogic with new Configuration
        of the Game.

        Args:
            config (Configuration): Game Configuration with information
                about number of rows, columns, mines.
        """
        log.debug('start_new_game, with config: %s', config)
        self._last_config = config
        self._game_instance = GameLogic(self._last_config)
        if self._on_game_status_update_callback:
            self._on_game_status_update_callback(
                self.get_game_info(ControllerActions.NEW_GAME))

    def reset_game(self) -> None:
        """Reset game state.

        Cleanups game state and returns game state to the initial
        values.
        """
        log.debug('reset_game, with config: %s', self._last_config)
        self._game_instance = GameLogic(self._last_config)
        if self._on_game_status_update_callback:
            self._on_game_status_update_callback(
                self.get_game_info(ControllerActions.RESET_GAME))

    def open_cell(self, row: int, column: int) -> None:
        """Open game field cell.

        Opens field cell and send notification about result of this
        open action.

        Args:
            row (int): number of the cell row.
            column (int): number of the cell column.
        """
        log.debug('open_cell, with row: %d, col: %d', row, column)
        if self._game_instance:
            self._game_instance.open_cell(row, column)
        if self._on_game_status_update_callback:
            self._on_game_status_update_callback(
                self.get_game_info(ControllerActions.CELL_OPENED))

    def flag_cell(self, row: int, column: int) -> None:
        """Put a flag to the cell.

        Puts flag to the field cell if the cell is not open and
        not flagged. If cell has a flag - flag will be removed.

        Args:
            row (int): number of the cell row.
            column (int): number of the cell column.
        """
        log.debug('flag_cell, with row: %d, col: %d', row, column)
        if self._game_instance:
            self._game_instance.flag_cell(row, column)
        if self._on_game_status_update_callback:
            self._on_game_status_update_callback(
                self.get_game_info(ControllerActions.CELL_FLAGGED))

    def get_game_info(self,
                      marker: ControllerActions | None = None
                      ) -> GameInformation | None:
        """Return game information.

        Retrieves all the information from current game and saves it
        in the GameInformation object to be used later.

        Args:
            marker (ControllerActions | None, optional): Marker to
                pass additional info about when this method was called.
                For example all the callbacks put information in which
                method was created game info (new game, reset, etc).
                Defaults to None.

        Returns:
            GameInformation | None: Object with game state information.
        """
        log.debug('get_game_info')
        if self._game_instance:
            info = GameInformation(
                number_of_rows=self._game_instance.rows,
                number_of_columns=self._game_instance.columns,
                number_of_mines=self._game_instance.number_of_mines,
                number_of_flags_left=self._game_instance.number_of_flags,
                game_field=self._game_instance.field,
                is_finished=self._game_instance.is_game_finished,
                is_player_win=self._game_instance.is_player_win,
                controller_action=marker
            )
            log.debug('get_game_info, info: %s', info)
            return info
        else:
            log.debug('get_game_info, info: None')
            return None
