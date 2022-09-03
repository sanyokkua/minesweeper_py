""" """
import logging

from minesweeper_core.data.cell import Cell

log: logging.Logger = logging.getLogger(__name__)


def is_alone_cell(field_cell: Cell) -> bool:
    """_summary_

    Args:
        field_cell (Cell): _description_

    Returns:
        bool: _description_
    """
    log.debug('is_alone_cell. cell: %s', field_cell)
    return (not field_cell.has_mine
            and not field_cell.is_open
            and not field_cell.has_flag
            and field_cell.neighbour_mines == 0)


def has_neighbour_mines(field_cell: Cell) -> bool:
    """_summary_

    Args:
        field_cell (Cell): _description_

    Returns:
        bool: _description_
    """
    log.debug('has_neighbour_mines. cell: %s', field_cell)
    return (not field_cell.has_mine
            and not field_cell.is_open
            and not field_cell.has_flag
            and field_cell.neighbour_mines > 0)


def get_neighbour_coordinates(current_coordinate: tuple[int, int],
                              number_of_rows: int,
                              number_of_columns: int) -> set[tuple[int, int]]:
    """_summary_

    Args:
        current_coordinate (tuple[int, int]): _description_
        number_of_rows (int): _description_
        number_of_columns (int): _description_

    Returns:
        set[tuple[int, int]]: _description_
    """
    # ( 0 0 ) ( 0 1 ) ( 0 2 )    ( -1 -1 ) ( -1 +0 ) ( -1 +1 )
    # ( 1 0 ) ( 1 1 ) ( 1 2 ) -> ( +0 -1 ) (  1  1 ) ( +0 +1 )
    # ( 2 0 ) ( 2 1 ) ( 2 2 )    ( +1 -1 ) ( +1 +0 ) ( +1 +1 )
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
        is_current_cell: bool = neighbour_row == row and neighbour_col == column
        if is_not_valid_row or is_not_valid_col or is_current_cell:
            log.debug(
                'get_neighbour_coordinates.is_not_valid_row or is_not_valid_col or is_current_cell')
            continue  # Filter coordinates that are not valid
        result_set.add((neighbour_row, neighbour_col))
    log.debug('get_neighbour_coordinates. result num: %d', len(result_set))
    return result_set
