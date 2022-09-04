"""Module contains ControllerActions class."""
import logging

from minesweeper_core.data.cell import Cell

log: logging.Logger = logging.getLogger(__name__)


def is_alone_cell(field_cell: Cell) -> bool:
    """Validate if the cell is alone.

    The main idea is that current cell:
        1) doesn't have mine
        2) is not opened
        4) doesn't have a flag
        5) doesn't have mines around
    With conditions above it means that cell can be processed and opened
    as alone cell (opening of the neighbour cell should be triggered).

    Args:
        field_cell (Cell): cell to be processed.

    Returns:
        bool: result of the condition check.
    """
    log.debug('is_alone_cell. cell: %s', field_cell)
    return (not field_cell.has_mine
            and not field_cell.is_open
            and not field_cell.has_flag
            and field_cell.neighbour_mines == 0)


def has_neighbour_mines(field_cell: Cell) -> bool:
    """Validate if the cell is not alone.

    The main idea is that current cell:
        1) doesn't have mine
        2) is not opened
        4) doesn't have a flag
        5) have mines around
    With conditions above it means that cell can be processed and opened
    as alone cell (opening of the neighbour cell should be triggered).

    Args:
        field_cell (Cell): cell to be processed.

    Returns:
        bool: result of the condition check.
    """
    log.debug('has_neighbour_mines. cell: %s', field_cell)
    return (not field_cell.has_mine
            and not field_cell.is_open
            and not field_cell.has_flag
            and field_cell.neighbour_mines > 0)


def get_neighbour_coordinates(current_coordinate: tuple[int, int],
                              number_of_rows: int,
                              number_of_columns: int) -> set[tuple[int, int]]:
    """Find coordinates of the neighbours to the passed coordinate.

    Builds a set (list) of the coordinates that should be in the cells
    around passed cell (current_coordinate).
    The logic to build and validate coordinates that will cover cells
    around and filter coordinates that can be out of the field measures.

    ( 0 0 ) ( 0 1 ) ( 0 2 )    ( -1 -1 ) ( -1 +0 ) ( -1 +1 )
    ( 1 0 ) ( 1 1 ) ( 1 2 ) -> ( +0 -1 ) (  1  1 ) ( +0 +1 )
    ( 2 0 ) ( 2 1 ) ( 2 2 )    ( +1 -1 ) ( +1 +0 ) ( +1 +1 )

    Args:
        current_coordinate (tuple[int, int]): cell coordinates.
        number_of_rows (int): field number of rows.
        number_of_columns (int): field number of columns.

    Returns:
        set[tuple[int, int]]: set of the built coordinates.
    """
    log.debug('get_neighbour_coordinates. current: %s', current_coordinate)
    row, column = current_coordinate
    coordinate_modifiers: set[tuple[int, int]] = {
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    }
    result_set: set[tuple[int, int]] = set()
    for row_modifier, column_modifier in coordinate_modifiers:
        neighbour_row: int = row + row_modifier
        neighbour_col: int = column + column_modifier
        is_not_valid_row: bool = (
                (neighbour_row < 0) or (neighbour_row >= number_of_rows))
        is_not_valid_col: bool = ((neighbour_col < 0) or (
                neighbour_col >= number_of_columns))
        is_current_cell: bool = (neighbour_row == row
                                 and neighbour_col == column)
        if is_not_valid_row or is_not_valid_col or is_current_cell:
            log.debug('Filter coordinates that are not valid')
            continue
        result_set.add((neighbour_row, neighbour_col))
    log.debug('get_neighbour_coordinates. result num: %d', len(result_set))
    return result_set
