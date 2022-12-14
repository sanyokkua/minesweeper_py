"""Module contains Field class."""
from dataclasses import dataclass

from minesweeper_core.data.cell import Cell
from minesweeper_core.data.field_configuration import Configuration


@dataclass(repr=True, frozen=True)
class Field:
    """Field data transfer object."""

    field_config: Configuration
    field_cells: dict[tuple[int, int], Cell]
