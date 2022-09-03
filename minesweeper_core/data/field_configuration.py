"""  """
from dataclasses import dataclass


@dataclass(frozen=True)
class Configuration:
    """ """
    number_of_rows: int = 9
    number_of_columns: int = 9
    number_of_mines: int = 10

    def __repr__(self) -> str:
        """_summary_

        Returns:
            _type_: _description_
        """
        return f'{self.number_of_rows}x{self.number_of_columns}, mines={self.number_of_mines}'
