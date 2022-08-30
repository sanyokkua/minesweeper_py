from minesweeper_core.data.field_configuration import Configuration

BEGINNER: Configuration = Configuration(number_of_rows=9, number_of_columns=9, number_of_mines=10)
INTERMEDIATE: Configuration = Configuration(number_of_rows=16, number_of_columns=16, number_of_mines=40)
ADVANCED: Configuration = Configuration(number_of_rows=24, number_of_columns=24, number_of_mines=99)
