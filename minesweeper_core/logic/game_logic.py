import logging
import random

from minesweeper_core.data.cell import Cell
from minesweeper_core.data.field import Field
from minesweeper_core.data.field_configuration import Configuration

log: logging.Logger = logging.getLogger(__name__)


class GameLogic:
    def __init__(self, game_config: Configuration) -> None:
        self._game_field: Field = Field(game_config, {})
        self._is_first_time_open = True
        self._is_game_finished = False
        self._is_player_win = False
        self._init_field()

    def _init_field(self) -> None:
        rows = self.rows
        cols = self.columns
        for row in range(rows):
            for col in range(cols):
                coordinate: tuple[int, int] = (row, col)
                cell: Cell = Cell(row, col)
                self.field[coordinate] = cell

    @property
    def rows(self) -> int:
        return self._game_field.field_config.number_of_rows

    @property
    def columns(self) -> int:
        return self._game_field.field_config.number_of_columns

    @property
    def field(self) -> dict[tuple[int, int], Cell]:
        return self._game_field.field_cells

    @property
    def is_game_finished(self) -> bool:
        return self._is_game_finished

    @property
    def is_player_win(self) -> bool:
        return self._is_player_win

    def open_cell(self, row: int, column: int) -> None:
        if self._is_first_time_open:
            self._open_cell((row, column))
            self._put_mines()
            self._is_first_time_open = False
            self._count_neighbour_mines_for_all_field()
        else:
            self._open_cell((row, column))

    def _open_cell(self, coordinate: tuple[int, int]) -> None:
        cell: Cell = self.field[coordinate]
        has_mine: bool = cell.has_mine
        has_flag: bool = cell.has_flag
        is_open: bool = cell.is_open
        neighbour_mines: int = cell.neighbour_mines

        if has_mine:
            self._finish_game(is_player_exploded=True)
        elif has_flag:
            cell.has_flag = False
        elif is_open:
            log.warning(f'Try of open already opened cell, {coordinate}')
        else:
            cell.is_open = True
            cell.has_flag = False
            if neighbour_mines == 0:
                self._open_neighbour_cells(coordinate)

    def _count_neighbour_mines_for_all_field(self) -> None:
        for cell in self.field.values():
            self._count_neighbour_mines_for_cell(cell)

    def _count_neighbour_mines_for_cell(self, cell: Cell) -> None:
        neighbours = self._get_neighbour_cells(cell.row, cell.column)
        count: int = 0
        for neighbour_cell in neighbours.values():
            if neighbour_cell.has_mine:
                count += 1
        cell.neighbour_mines = count

    def _get_neighbour_cells(self, row: int, column: int) -> dict[tuple[int, int], Cell]:
        # ( 0 0 ) ( 0 1 ) ( 0 2 )    ( -1 -1 ) ( -1 +0 ) ( -1 +1 )
        # ( 1 0 ) ( 1 1 ) ( 1 2 ) -> ( +0 -1 ) (  1  1 ) ( +0 +1 )
        # ( 2 0 ) ( 2 1 ) ( 2 2 )    ( +1 -1 ) ( +1 +0 ) ( +1 +1 )
        coordinates_diff: set = {
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        }
        result_dictionary: dict[tuple[int, int], Cell] = {}
        for row_diff, col_diff in coordinates_diff:
            neighbour_row: int = row + row_diff
            neighbour_col: int = column + col_diff
            is_not_valid_row: bool = ((neighbour_row < 0) or (neighbour_row >= self.rows))
            is_not_valid_col: bool = ((neighbour_col < 0) or (neighbour_col >= self.columns))
            is_current_cell: bool = neighbour_row == row and neighbour_col == column
            if is_not_valid_row or is_not_valid_col or is_current_cell:
                continue  # Filter coordinates that are out of bounds or current cell
            try:
                neighbour_cell: Cell = self.field[(neighbour_row, neighbour_col)]
                result_dictionary[(neighbour_row, neighbour_col)] = neighbour_cell
            except KeyError as err:
                log.debug('Coordinate is not valid, %s', err)
        return result_dictionary

    def _put_mines(self) -> None:
        number_of_mines = self._game_field.field_config.number_of_mines
        coordinates: set[tuple[int, int]] = set()
        while number_of_mines > 0:
            coord: tuple[int, int] = random.choice(list(self.field.keys()))
            if coord in coordinates or self.field[coord].is_open:
                continue  # We do not to have coordinates that already in the list or
                # coordinates of the cell that were already opened (In the beginning of the game)
            else:
                coordinates.add(coord)
                number_of_mines -= 1
        for cell_coordinate in coordinates:
            self.field[cell_coordinate].has_mine = True

    def _finish_game(self, is_player_exploded: bool = False) -> None:
        for cell in self.field.values():
            cell.is_open = True
        self._is_game_finished = True
        self._is_player_win = not is_player_exploded

    def _open_neighbour_cells(self, coordinate: tuple[int, int]) -> None:
        pass  # TODO: Implement flood-fill algorithm
