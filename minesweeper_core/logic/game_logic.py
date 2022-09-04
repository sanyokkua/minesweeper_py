"""Module contains GameLogic class."""
import logging
import random

import minesweeper_core.logic.utils as utils
from minesweeper_core.data.cell import Cell
from minesweeper_core.data.field import Field
from minesweeper_core.data.field_configuration import Configuration
from minesweeper_core.logic.exceptions import IncorrectCoordinatesException

log: logging.Logger = logging.getLogger(__name__)

FieldDict = dict[tuple[int, int], Cell]


class GameLogic:
    """Class encapsulates logic of the game."""

    def __init__(self, game_config: Configuration) -> None:
        """Initialize GameLogic with the passed configuration.

        Args:
            game_config (Configuration): configuration contains
                parameters of the game session as size of field and
                number of mines.
        """
        log.debug('Initializing game')
        self._game_field: Field = Field(game_config, {})
        self._is_first_time_open = True
        self._is_game_finished = False
        self._is_player_win = False
        self._flags_number = game_config.number_of_mines
        self._init_field()
        log.debug('field: %s, first_time: %s, finished: %s, win: %s',
                  self._game_field,
                  self._is_first_time_open,
                  self.is_game_finished,
                  self.is_player_win)

    def _init_field(self) -> None:
        """Initialize field with default values."""
        rows: int = self.rows
        cols: int = self.columns
        for row in range(rows):
            for col in range(cols):
                coordinate: tuple[int, int] = (row, col)
                cell: Cell = Cell(row, col)
                self.field[coordinate] = cell
        log.debug('Field inited with - rows: %d, cols: %d, total: %d',
                  rows, cols, len(self.field))

    @property
    def rows(self) -> int:
        """Return number of rows.

        Returns:
            int: number of rows.
        """
        return self._game_field.field_config.number_of_rows

    @property
    def columns(self) -> int:
        """Return number of columns.

        Returns:
            int: number of columns.
        """
        return self._game_field.field_config.number_of_columns

    @property
    def field(self) -> FieldDict:
        """Return field.

        Returns:
            FieldDict: current field.
        """
        return self._game_field.field_cells

    @property
    def number_of_mines(self) -> int:
        """Return number of mines.

        Returns:
            int: number of mines.
        """
        return self._game_field.field_config.number_of_mines

    @property
    def number_of_flags(self) -> int:
        """Return number of available flags.

        Returns:
            int: number of flags.
        """
        return self._flags_number

    @property
    def is_game_finished(self) -> bool:
        """Return game state status.

        If game is finished - True will be returned.
        False will be return if game still alive.

        Returns:
            bool: finished game status.
        """
        return self._is_game_finished

    @property
    def is_player_win(self) -> bool:
        """Return status of the player in the game.

        If player has not opened cell with bomb/mine, then player status
        will be True (is_player_win will return True).
        If player exploded - value will be False.

        Returns:
            bool: player win status.
        """
        return self._is_player_win

    def open_cell(self, row: int, column: int) -> None:
        """Open cell by coordinates.

        Cell with coordinates (row, column) will be opened and status of
        the game will be reprocessed.
        After opening the cell, game will check if game is not finished
        and neighbour cells will be opened also if conditions are valid
        for it.
        For first open time - mines will be set to random cells
        excluding current cell coordinates.

        Args:
            row (int): cell row number.
            column (int): cell column number.
        """
        log.debug('Open Cell, (%d, %d)', row, column)
        self._validate_coordinates(row, column)
        current_coordinate: tuple[int, int] = (row, column)
        if self._is_first_time_open:
            log.debug('Open Cell, _is_first_time_open = True')
            self._put_mines(current_coordinate)
            self._count_neighbour_mines_for_all_field()
            self._is_first_time_open = False
        self._open_cell(current_coordinate)
        self._process_current_game_state()

    def flag_cell(self, row: int, column: int) -> None:
        """Put or remove flag from the cell.

        If cell is not open (already) and doesn't have a flag - method
        will add flag to this cell.
        If cell is not open and has a flag - flag will be removed from
        this cell.

        Args:
            row (int): cell row number.
            column (int): cell column number.
        """
        log.debug('flag_cell, (%d, %d)', row, column)
        self._validate_coordinates(row, column)
        cell: Cell = self.field[(row, column)]
        log.debug('flag_cell, (%d, %d) flag_before -> %s',
                  row, column, cell.has_flag)
        if cell.has_flag:
            cell.has_flag = False
            self._flags_number += 1
        elif not cell.has_flag and self._flags_number > 0 and not cell.is_open:
            cell.has_flag = True
            self._flags_number -= 1
        log.debug('flag_cell, (%d, %d) flag_after -> %s',
                  row, column, cell.has_flag)

    def _open_cell(self, coordinate: tuple[int, int]) -> None:
        """Open cell.

        Validate preconditions and open cell, check game state, etc.

        Args:
            coordinate (tuple[int, int]): coordinate of opening cell
                as tuple[row, column]
        """
        log.debug('_open_cell.begin')
        cell: Cell = self.field[coordinate]
        has_mine: bool = cell.has_mine
        has_flag: bool = cell.has_flag
        is_open: bool = cell.is_open

        if has_mine:
            log.debug('_open_cell.has_mine')
            self._finish_game(is_player_exploded=True)
        elif has_flag:
            log.debug('_open_cell.begin')
            cell.has_flag = False
        elif is_open:
            log.debug('_open_cell.has_flag')
            log.warning('Try of open already opened cell, %s', coordinate)
        else:
            log.debug('_open_cell. is opening')
            cell.has_flag = False
            self._open_this_and_neighbour_cells(coordinate)
        log.debug('_open_cell.end')

    def _put_mines(self, current_coordinate: tuple[int, int]) -> None:
        """Put mines to the field.

        Put to the field mines in random positions excluding passed
        coordinate.

        Args:
            current_coordinate (tuple[int, int]): coordinate of opening
                cell as tuple[row, column].
        """
        log.debug('_put_mines, skip coordinate: %s', current_coordinate)
        number_of_mines: int = self._game_field.field_config.number_of_mines
        coordinates: set[tuple[int, int]] = set()
        while len(coordinates) < number_of_mines:
            coord: tuple[int, int] = random.choice(list(self.field.keys()))
            if coord not in coordinates and coord != current_coordinate:
                log.debug('_put_mines, add coordinate: %s', coord)
                coordinates.add(coord)
        for cell_coordinate in coordinates:
            cell = self.field[cell_coordinate]
            cell.has_mine = True
            log.debug('_put_mines, put mine to coordinate: %s, has_mine: %s',
                      cell_coordinate,
                      cell.has_mine)

    def _count_neighbour_mines_for_all_field(self) -> None:
        """Count mines for cells in the field."""
        log.debug('_count_neighbour_mines_for_all_field')
        for cell in self.field.values():
            self._count_neighbour_mines_for_cell(cell)

    def _finish_game(self, is_player_exploded: bool = False) -> None:
        """Check game state.

        Check each cell in the field to validate condition of the
        finished game. If is_player_exploded passed True, is_player_win
        will be set to False.

        Args:
            is_player_exploded (bool, optional): shows of the player
                status. Defaults to False.
        """
        log.debug('_finish_game, is_player_win: %s', is_player_exploded)
        for cell in self.field.values():
            cell.is_open = True
        self._is_game_finished = True
        self._is_player_win = not is_player_exploded
        if self._is_player_win:
            for cell in self.field.values():
                if cell.has_mine:
                    cell.has_flag = True
        log.debug(
            '_finish_game. Result {_is_game_finished: %s, _is_player_win: %s}',
            self._is_game_finished, self._is_player_win)

    def _open_this_and_neighbour_cells(self,
                                       coordinate: tuple[int, int]) -> None:
        """Open current and neighbour cells.

        If the conditions are appropriate for opening neighbour cells,
        they will be opened in addition to the cell represented by
        passed coordinate.

        Args:
            coordinate (tuple[int, int]): current cell coordinate.
        """
        log.debug('_open_this_and_neighbour_cells, coordinate: %s', coordinate)
        if self.field[coordinate].neighbour_mines > 0:
            self.field[coordinate].is_open = True
            log.debug('skip opening neighbours, because has neighbour mines')
            return
        queue: set[tuple[int, int]] = set()
        queue.add(coordinate)
        while len(queue) > 0:
            pop_coordinate: tuple[int, int] = queue.pop()
            log.debug('processing pop_coordinate: %s', pop_coordinate)
            current_cell: Cell = self.field[pop_coordinate]
            if utils.is_alone_cell(current_cell):
                log.debug('utils.is_alone_cell(current_cell)')
                current_cell.is_open = True
                neighbours = utils.get_neighbour_coordinates(
                    pop_coordinate, self.rows, self.columns)
                for new_coordinate in neighbours:
                    queue.add(new_coordinate)
            elif utils.has_neighbour_mines(current_cell):
                log.debug('utils.has_neighbour_mines(current_cell)')
                current_cell.is_open = True

    def _count_neighbour_mines_for_cell(self, cell: Cell) -> None:
        """Find and count mines around passed cell.

        Args:
            cell (Cell): current cell that is processing.
        """
        log.debug('_count_neighbour_mines_for_cell, cell: %s', cell)
        neighbours = self._get_neighbour_cells(cell.row, cell.column)
        count: int = 0
        for neighbour_cell in neighbours.values():
            if neighbour_cell.has_mine:
                count += 1
        cell.neighbour_mines = count
        log.debug('cell: %s, mines_around: %d', cell, cell.neighbour_mines)

    def _get_neighbour_cells(self, row: int, column: int) -> FieldDict:
        """Find and return all the neighbour cell to the passed coordinates.

        Args:
            row (int): row number.
            column (int): column number.

        Returns:
            FieldDict: dictionary that represents field.
        """
        log.debug('_get_neighbour_cells. (%d, %d)', row, column)
        neighbours = utils.get_neighbour_coordinates(
            (row, column), self.rows, self.columns)
        result_dictionary: FieldDict = {}
        for n_coordinate in neighbours:
            result_dictionary[n_coordinate] = self.field[n_coordinate]
        log.debug(
            '_get_neighbour_cells. for (%d, %d), number of neighbours: %d',
            row, column, len(result_dictionary))
        return result_dictionary

    def _validate_coordinates(self, row: int, column: int) -> None:
        """Validate passed coordinates.

        Args:
            row (int): row number.
            column (int): column number.

        Raises:
            IncorrectCoordinatesException: raised if the coordinates has
                incorrect values.
        """
        log.debug('Validation of (%d, %d)', row, column)
        is_valid_row: bool = 0 <= row < self.rows
        is_valid_col: bool = 0 <= column < self.columns
        log.debug('Validation result - is_valid_row: %s, is_valid_col: %s)',
                  is_valid_row, is_valid_col)
        if not is_valid_row or not is_valid_col:
            raise IncorrectCoordinatesException('Coordinates are not valid')

    def _process_current_game_state(self) -> None:
        """Check if the game has finished state.

        Gather all the game information and check conditions that will
        say if the game finished or can be continued.
        """
        log.debug('_process_current_game_state.begin')
        config = self._game_field.field_config
        expected_number_of_mines: int = config.number_of_mines
        expected_number_of_cells: int = self.rows * self.columns
        log.debug('num_mines: %d, num_cells: %d',
                  expected_number_of_mines,
                  expected_number_of_cells)
        count_opened_cells: int = 0
        for cell in self.field.values():
            if cell.is_open:
                count_opened_cells += 1
        log.debug('opened: %d', count_opened_cells)
        total_num: int = count_opened_cells + expected_number_of_mines
        log.debug('total_num: %d', total_num)
        if total_num == expected_number_of_cells:
            log.debug('Game is Finished without flags')
            self._finish_game(is_player_exploded=False)
        log.debug('_process_current_game_state.begin')
