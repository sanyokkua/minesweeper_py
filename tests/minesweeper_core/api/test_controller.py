import unittest.mock as mock

from minesweeper_core.api.controller import MinesweeperController
from minesweeper_core.constants.default_configurations import BEGINNER, INTERMEDIATE
from minesweeper_core.data.field_configuration import Configuration
from minesweeper_core.logic.game_logic import GameLogic


class TestMinesweeperController:
    def test_init(self) -> None:
        mock_method = mock.Mock()
        game = MinesweeperController(on_game_status_update_callback=mock_method)

        assert game._game_instance is None
        assert game._last_config is BEGINNER
        assert game._on_game_status_update_callback is mock_method
        mock_method.assert_not_called()

    @mock.patch('minesweeper_core.api.controller.GameLogic')
    def test_start_new_game(self, game_logic_mock) -> None:
        mock_callback = mock.Mock()
        mock_game_logic = mock.Mock()
        game_logic_mock.return_value = mock_game_logic
        field_dict = {}
        attrs = {
            'rows.return_value': 25,
            'columns.return_value': 39,
            'number_of_mines.return_value': 17,
            'number_of_flags.return_value': 19,
            'field.return_value': field_dict,
            'is_game_finished.return_value': True,
            'is_player_win.return_value': True
        }
        mock_game_logic.configure_mock(**attrs)

        game = MinesweeperController(on_game_status_update_callback=mock_callback)
        game.start_new_game(INTERMEDIATE)

        assert game._last_config is INTERMEDIATE
        assert game._game_instance is mock_game_logic
        mock_callback.assert_called_once()

    @mock.patch('minesweeper_core.api.controller.GameLogic')
    def test_reset_game(self, game_logic_mock) -> None:
        mock_callback = mock.Mock()
        mock_game_logic = mock.Mock()
        game_logic_mock.return_value = mock_game_logic
        field_dict = {}
        attrs = {
            'rows.return_value': 25,
            'columns.return_value': 39,
            'number_of_mines.return_value': 17,
            'number_of_flags.return_value': 19,
            'field.return_value': field_dict,
            'is_game_finished.return_value': True,
            'is_player_win.return_value': True
        }
        mock_game_logic.configure_mock(**attrs)

        game = MinesweeperController(on_game_status_update_callback=mock_callback)
        game.start_new_game(INTERMEDIATE)
        mock_callback.assert_called()

        game.reset_game()
        assert game._last_config is INTERMEDIATE
        assert game._game_instance is mock_game_logic
        mock_callback.assert_called()

    @mock.patch('minesweeper_core.api.controller.GameLogic')
    def test_open_cell(self, game_logic_mock) -> None:
        mock_callback = mock.Mock()
        mock_open = mock.Mock()
        mock_game_logic = mock.Mock()
        field_dict = {}
        attrs = {
            'open_cell': mock_open,
            'rows.return_value': 25,
            'columns.return_value': 39,
            'number_of_mines.return_value': 17,
            'number_of_flags.return_value': 19,
            'field.return_value': field_dict,
            'is_game_finished.return_value': True,
            'is_player_win.return_value': True
        }
        mock_game_logic.configure_mock(**attrs)
        game_logic_mock.return_value = mock_game_logic

        game = MinesweeperController(on_game_status_update_callback=mock_callback)
        game.start_new_game(INTERMEDIATE)
        mock_callback.assert_called()

        game.open_cell(2, 5)
        assert game._last_config is INTERMEDIATE
        assert game._game_instance is mock_game_logic
        mock_open.assert_called_once_with(2, 5)

    @mock.patch('minesweeper_core.api.controller.GameLogic')
    def test_flag_cell(self, game_logic_mock) -> None:
        mock_callback = mock.Mock()
        mock_flag = mock.Mock()
        mock_game_logic = mock.Mock()
        field_dict = {}
        attrs = {
            'flag_cell': mock_flag,
            'rows.return_value': 25,
            'columns.return_value': 39,
            'number_of_mines.return_value': 17,
            'number_of_flags.return_value': 19,
            'field.return_value': field_dict,
            'is_game_finished.return_value': True,
            'is_player_win.return_value': True
        }
        mock_game_logic.configure_mock(**attrs)
        game_logic_mock.return_value = mock_game_logic

        game = MinesweeperController(on_game_status_update_callback=mock_callback)
        game.start_new_game(INTERMEDIATE)
        mock_callback.assert_called()

        game.flag_cell(2, 5)
        assert game._last_config is INTERMEDIATE
        assert game._game_instance is mock_game_logic
        mock_flag.assert_called_once_with(2, 5)

    @mock.patch('minesweeper_core.api.controller.GameLogic')
    def test_get_game_info(self, game_logic_mock) -> None:
        config = Configuration(
            number_of_rows=23,
            number_of_columns=17,
            number_of_mines=5
        )
        game_logic = GameLogic(config)

        mock_callback = mock.Mock()
        game_logic_mock.return_value = game_logic

        game = MinesweeperController(on_game_status_update_callback=mock_callback)
        game.start_new_game(INTERMEDIATE)
        mock_callback.assert_called()

        info = game.get_game_info()
        assert game._last_config is INTERMEDIATE
        assert game._game_instance is game_logic
        assert info.number_of_rows == config.number_of_rows
        assert info.number_of_columns == config.number_of_columns
        assert info.number_of_mines == config.number_of_mines
        assert info.number_of_flags_left == config.number_of_mines
        assert info.game_field is game._game_instance.field
        assert not info.is_finished
        assert not info.is_player_win

    def test_get_game_info_just_created(self) -> None:
        game = MinesweeperController()
        info = game.get_game_info()

        assert game._last_config is BEGINNER
        assert info is None
