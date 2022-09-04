"""Module contains Configuration class."""
from dataclasses import dataclass


@dataclass(frozen=True, repr=True)
class Configuration:
    """Configuration data transfer object."""

    number_of_rows: int = 9
    number_of_columns: int = 9
    number_of_mines: int = 10
