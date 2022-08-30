from dataclasses import dataclass


@dataclass(repr=True)
class Cell:
    row: int
    column: int
    neighbour_mines: int = 0
    is_open: bool = False
    has_mine: bool = False
    has_flag: bool = False
