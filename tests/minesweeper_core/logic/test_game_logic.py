import pytest

from minesweeper_core.constants.default_configurations import ADVANCED, \
    BEGINNER, INTERMEDIATE
from minesweeper_core.data.field_configuration import Configuration
from minesweeper_core.logic.exceptions import IncorrectCoordinatesException
from minesweeper_core.logic.game_logic import GameLogic


class TestGameLogic:
    def test_init_with_beginner_config(self) -> None:
        config = BEGINNER
        game = GameLogic(BEGINNER)
        game_rows = game.rows
        game_cols = game.columns
        game_mines = game._game_field.field_config.number_of_mines

        config_number_of_mines = config.number_of_mines
        config_number_of_rows = config.number_of_rows
        config_number_of_cols = config.number_of_columns

        expected_number_of_mines = 10
        expected_number_of_rows = 9
        expected_number_of_cols = 9
        expected_number_of_cells = expected_number_of_rows * expected_number_of_cols

        assert expected_number_of_rows == config_number_of_rows
        assert expected_number_of_cols == config_number_of_cols
        assert expected_number_of_mines == config_number_of_mines

        assert expected_number_of_rows == game_rows
        assert expected_number_of_cols == game_cols
        assert expected_number_of_mines == game_mines
        assert expected_number_of_cells == len(game.field)

        for cell in game.field.values():
            assert not cell.has_flag
            assert not cell.has_mine
            assert not cell.is_open
            assert cell.neighbour_mines == 0

    def test_init_with_intermediate_config(self) -> None:
        config = INTERMEDIATE
        game = GameLogic(config)
        game_rows = game.rows
        game_cols = game.columns
        game_mines = game._game_field.field_config.number_of_mines

        config_number_of_mines = config.number_of_mines
        config_number_of_rows = config.number_of_rows
        config_number_of_cols = config.number_of_columns

        expected_number_of_mines = 40
        expected_number_of_rows = 16
        expected_number_of_cols = 16
        expected_number_of_cells = expected_number_of_rows * expected_number_of_cols

        assert expected_number_of_rows == config_number_of_rows
        assert expected_number_of_cols == config_number_of_cols
        assert expected_number_of_mines == config_number_of_mines

        assert expected_number_of_rows == game_rows
        assert expected_number_of_cols == game_cols
        assert expected_number_of_mines == game_mines
        assert expected_number_of_cells == len(game.field)

        for cell in game.field.values():
            assert not cell.has_flag
            assert not cell.has_mine
            assert not cell.is_open
            assert cell.neighbour_mines == 0

    def test_init_with_advanced_config(self) -> None:
        config = ADVANCED
        game = GameLogic(config)
        game_rows = game.rows
        game_cols = game.columns
        game_mines = game._game_field.field_config.number_of_mines

        config_number_of_mines = config.number_of_mines
        config_number_of_rows = config.number_of_rows
        config_number_of_cols = config.number_of_columns

        expected_number_of_mines = 99
        expected_number_of_rows = 24
        expected_number_of_cols = 24
        expected_number_of_cells = expected_number_of_rows * expected_number_of_cols

        assert expected_number_of_rows == config_number_of_rows
        assert expected_number_of_cols == config_number_of_cols
        assert expected_number_of_mines == config_number_of_mines

        assert expected_number_of_rows == game_rows
        assert expected_number_of_cols == game_cols
        assert expected_number_of_mines == game_mines
        assert expected_number_of_cells == len(game.field)

        for cell in game.field.values():
            assert not cell.has_flag
            assert not cell.has_mine
            assert not cell.is_open
            assert cell.neighbour_mines == 0

    def test_get_property_rows(self) -> None:
        game = GameLogic(BEGINNER)
        assert game.rows == 9
        assert isinstance(game.rows, int)

    def test_get_property_columns(self) -> None:
        game = GameLogic(BEGINNER)
        assert game.columns == 9
        assert isinstance(game.columns, int)

    def test_get_property_field(self) -> None:
        game = GameLogic(BEGINNER)
        assert game.field is not None
        assert isinstance(game.field, dict)

    def test_get_property_is_game_finished(self) -> None:
        game = GameLogic(BEGINNER)
        assert not game.is_game_finished
        assert isinstance(game.is_game_finished, bool)

    def test_get_property_is_player_win(self) -> None:
        game = GameLogic(BEGINNER)
        assert not game.is_player_win
        assert isinstance(game.is_player_win, bool)

    def test_get_property_number_of_mines(self) -> None:
        game = GameLogic(BEGINNER)
        assert game.number_of_mines == 10
        assert isinstance(game.number_of_mines, int)

    def test_get_property_number_of_flags(self) -> None:
        game = GameLogic(BEGINNER)
        assert game.number_of_flags == 10
        assert isinstance(game.number_of_flags, int)

    def test_set_property_number_of_flags(self) -> None:
        game = GameLogic(BEGINNER)
        with pytest.raises(AttributeError):
            game.number_of_flags = 100

    def test_set_property_number_of_mines(self) -> None:
        game = GameLogic(BEGINNER)
        with pytest.raises(AttributeError):
            game.number_of_mines = 100

    def test_set_property_rows(self) -> None:
        game = GameLogic(BEGINNER)
        with pytest.raises(AttributeError):
            game.rows = 10

    def test_set_property_columns(self) -> None:
        game = GameLogic(BEGINNER)
        with pytest.raises(AttributeError):
            game.columns = 10

    def test_set_property_field(self) -> None:
        game = GameLogic(BEGINNER)
        with pytest.raises(AttributeError):
            game.field = {}

    def test_set_property_is_game_finished(self) -> None:
        game = GameLogic(BEGINNER)
        with pytest.raises(AttributeError):
            game.is_game_finished = True

    def test_set_property_is_player_win(self) -> None:
        game = GameLogic(BEGINNER)
        with pytest.raises(AttributeError):
            game.is_player_win = True

    def test_open_cell_first_time(self) -> None:
        game = GameLogic(BEGINNER)
        number_of_mines_in_field = 0
        number_of_opened_fields = 0
        for cell in game.field.values():
            if cell.has_mine:
                number_of_mines_in_field += 1
            if cell.is_open:
                number_of_opened_fields += 1

        assert number_of_mines_in_field == 0
        assert number_of_opened_fields == 0

        game.open_cell(0, 0)
        assert game.field[(0, 0)].is_open
        assert not game.field[(0, 0)].has_mine
        assert not game.field[(0, 0)].has_flag

        number_of_mines_in_field_after = 0
        number_of_opened_fields_after = 0
        for cell in game.field.values():
            if cell.has_mine:
                number_of_mines_in_field_after += 1
            if cell.is_open:
                number_of_opened_fields_after += 1

        assert number_of_mines_in_field_after == 10
        assert number_of_opened_fields_after >= 1

    def test_flag_cell(self) -> None:
        game = GameLogic(BEGINNER)
        game._put_mines = lambda coordinates: print(coordinates)
        game.field[(0, 0)].has_mine = True
        game.field[(5, 5)].has_mine = True
        game.field[(3, 3)].has_mine = True
        game.open_cell(0, 1)
        assert game._flags_number == BEGINNER.number_of_mines
        game.flag_cell(3, 1)
        game.flag_cell(0, 2)
        game.flag_cell(0, 3)
        assert game._flags_number == (BEGINNER.number_of_mines - 3)
        game.flag_cell(0, 4)
        game.flag_cell(0, 5)
        game.flag_cell(0, 6)
        game.flag_cell(0, 7)
        game.flag_cell(0, 8)
        assert game._flags_number == (BEGINNER.number_of_mines - 8)
        game.flag_cell(1, 0)
        game.flag_cell(1, 1)
        assert game._flags_number == (BEGINNER.number_of_mines - 10)
        game.flag_cell(1, 1)
        assert game._flags_number == (BEGINNER.number_of_mines - 9)
        game.flag_cell(1, 0)
        assert game._flags_number == (BEGINNER.number_of_mines - 8)
        game.flag_cell(0, 8)
        game.flag_cell(0, 7)
        game.flag_cell(0, 6)
        game.flag_cell(0, 5)
        game.flag_cell(0, 4)
        game.flag_cell(0, 3)
        game.flag_cell(0, 2)
        game.flag_cell(3, 1)
        assert game._flags_number == BEGINNER.number_of_mines

    def test__open_cell_has_mine(self) -> None:
        game = GameLogic(BEGINNER)
        game.open_cell(0, 0)
        game.field[(1, 1)].has_mine = True
        game.field[(1, 1)].has_flag = False
        game.field[(1, 1)].is_open = False
        game._open_cell((1, 1))

        assert game.is_game_finished
        assert not game.is_player_win
        assert game.field[(1, 1)].is_open

    def test__open_cell_has_flag(self) -> None:
        game = GameLogic(BEGINNER)
        game.open_cell(0, 0)
        game.field[(2, 2)].has_mine = False
        game.field[(2, 2)].has_flag = True
        game.field[(2, 2)].is_open = False
        game._open_cell((2, 2))

        assert not game.is_game_finished
        assert not game.is_player_win
        assert not game.field[(2, 2)].has_flag
        assert not game.field[(2, 2)].is_open

    def test__open_cell_normal_cell(self) -> None:
        game = GameLogic(BEGINNER)
        game.open_cell(0, 0)
        game.field[(3, 3)].has_mine = False
        game.field[(3, 3)].has_flag = False
        game.field[(3, 3)].is_open = False
        game._open_cell((3, 3))

        assert not game.is_game_finished
        assert not game.is_player_win
        assert game.field[(3, 3)].is_open

    def test__open_cell_already_opened_cell(self) -> None:
        game = GameLogic(BEGINNER)
        game.open_cell(0, 0)
        game.field[(4, 4)].has_mine = False
        game.field[(4, 4)].has_flag = False
        game.field[(4, 4)].is_open = True
        game._open_cell((4, 4))

        assert not game.is_game_finished
        assert not game.is_player_win
        assert game.field[(4, 4)].is_open

    def test__put_mines(self) -> None:
        game = GameLogic(BEGINNER)
        count_mines_before = 0
        for cell in game.field.values():
            if cell.has_mine:
                count_mines_before += 1

        game._put_mines((0, 0))

        count_mines_after = 0
        for cell in game.field.values():
            if cell.has_mine:
                count_mines_after += 1

        assert count_mines_before == 0
        assert count_mines_after > count_mines_before
        assert count_mines_after == BEGINNER.number_of_mines

    def test__open_neighbour_cells(self) -> None:
        config = Configuration(
            number_of_rows=5, number_of_columns=5, number_of_mines=3)
        game = GameLogic(config)
        # * - - - -     ->      * - - - -
        # - - - - -     ->      1 1 1 - -
        # - - - * -     ->      - - 1 * -
        # - - - - -     ->      - - 1 2 -
        # - - - - *     ->      - - - 1 *
        game._is_first_time_open = False
        game.field[(0, 0)].has_mine = True
        game.field[(2, 3)].has_mine = True
        game.field[(4, 4)].has_mine = True
        game._open_this_and_neighbour_cells((0, 4))
        assert game.field[(2, 0)].is_open
        assert game.field[(3, 0)].is_open
        assert game.field[(4, 0)].is_open
        assert game.field[(2, 1)].is_open
        assert game.field[(3, 1)].is_open
        assert game.field[(4, 1)].is_open
        assert game.field[(4, 2)].is_open
        assert game.field[(1, 0)].is_open
        assert game.field[(1, 1)].is_open
        assert game.field[(1, 2)].is_open
        assert game.field[(2, 2)].is_open
        assert game.field[(3, 2)].is_open
        assert game.field[(3, 3)].is_open
        assert game.field[(4, 3)].is_open

    def test__validate_coordinates(self) -> None:
        game = GameLogic(BEGINNER)
        with pytest.raises(IncorrectCoordinatesException):
            game._validate_coordinates(-1, 0)
        with pytest.raises(IncorrectCoordinatesException):
            game._validate_coordinates(0, -1)
        with pytest.raises(IncorrectCoordinatesException):
            game._validate_coordinates(-1, -1)
        with pytest.raises(IncorrectCoordinatesException):
            game._validate_coordinates(9, 0)
        with pytest.raises(IncorrectCoordinatesException):
            game._validate_coordinates(0, 9)
        with pytest.raises(IncorrectCoordinatesException):
            game._validate_coordinates(9, 9)

    def test__process_current_game_state_without_flags(self) -> None:
        config = Configuration(
            number_of_rows=5, number_of_columns=5, number_of_mines=3)
        game = GameLogic(config)
        game._put_mines = lambda _: print()
        # * - - - -
        # - - - - -
        # - - - * -
        # - - - - -
        # - - - - *
        game.field[(0, 0)].has_mine = True
        game.field[(2, 3)].has_mine = True
        game.field[(4, 4)].has_mine = True
        game.open_cell(4, 0)
        assert not game._is_game_finished
        assert not game._is_player_win
        game.open_cell(0, 1)
        assert not game._is_game_finished
        game.open_cell(0, 2)
        assert not game._is_game_finished
        game.open_cell(3, 4)
        assert not game._is_game_finished
        game.open_cell(3, 4)
        assert not game._is_game_finished
        game.open_cell(1, 3)
        assert not game._is_game_finished
        game.open_cell(0, 4)
        assert not game._is_game_finished
        game.open_cell(0, 3)
        assert not game._is_game_finished
        game.open_cell(2, 4)
        assert game._is_game_finished

    def test__process_current_game_state_with_flags(self) -> None:
        config = Configuration(
            number_of_rows=5, number_of_columns=5, number_of_mines=3)
        game = GameLogic(config)
        game._put_mines = lambda _: print()
        # * - - - -
        # - - - - -
        # - - - * -
        # - - - - -
        # - - - - *
        game.field[(0, 0)].has_mine = True
        game.field[(2, 3)].has_mine = True
        game.field[(4, 4)].has_mine = True
        game.open_cell(4, 0)
        game.flag_cell(0, 0)
        game.flag_cell(2, 3)
        game.flag_cell(4, 4)
        assert not game._is_game_finished
        assert not game._is_player_win
        game.open_cell(0, 1)
        assert not game._is_game_finished
        game.open_cell(0, 2)
        assert not game._is_game_finished
        game.open_cell(3, 4)
        assert not game._is_game_finished
        game.open_cell(3, 4)
        assert not game._is_game_finished
        game.open_cell(1, 3)
        assert not game._is_game_finished
        game.open_cell(0, 4)
        assert not game._is_game_finished
        game.open_cell(0, 3)
        assert not game._is_game_finished
        game.open_cell(2, 4)
        assert game._is_game_finished
