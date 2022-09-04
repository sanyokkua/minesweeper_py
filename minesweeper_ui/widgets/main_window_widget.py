"""Module contains QMainWindowMinesweeper class."""
import logging
import sys

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (QHBoxLayout, QLCDNumber, QLabel, QMainWindow,
                             QMenu, QMenuBar, QVBoxLayout, QWidget)

import minesweeper_ui.game_instance as instance
from minesweeper_core.api.dtos import GameInformation
from minesweeper_core.api.markers import ControllerActions
from minesweeper_core.constants.configurations import BEGINNER
from minesweeper_core.data.field_configuration import Configuration
from minesweeper_ui.widgets.custom_buttons import QResetButton
from minesweeper_ui.widgets.dialogs.new_game.dialog_widget import QDialogWidget
from minesweeper_ui.widgets.field.field_widget import QWidgetFieldMinesweeper

log: logging.Logger = logging.getLogger(__name__)


class QMainWindowMinesweeper(QMainWindow):
    """Implementation of the main window widget of the game.

    Args:
        QMainWindow (_type_): parent class.
    """

    def __init__(self) -> None:
        """Initialize default values and configuration."""
        super().__init__()
        log.debug('__init__')
        self._timer: QTimer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_timer_update)
        self._timer_time: int = 0

        self.setWindowTitle('Minesweeper')
        self._field_widget: QWidgetFieldMinesweeper = QWidgetFieldMinesweeper()
        self._init_menu_items()
        self._create_window_container_widget_and_layout()
        self._create_control_widget_container_and_layout()
        self._create_control_widgets()
        self._add_control_widgets_to_layout()
        self._configure_control_widgets()
        self._add_reset_game_push_button_signal_handler()
        self._add_game_menu_actions_signal_handler()

        self._window_container_widget_layout.addWidget(self.menuBar())
        self._window_container_widget_layout.addWidget(
            self._main_control_widget)
        self._window_container_widget_layout.addWidget(self._field_widget)

        self.setCentralWidget(self._window_container_widget)

        min_size: QSize = QSize(540, 400)
        self.setMinimumSize(min_size)
        self.resize(min_size)

        instance.subscribe_to_updates(self._on_game_status_update_callback)
        instance.CONTROLLER.start_new_game(BEGINNER)

        QTimer.singleShot(0, self._reset_game_push_button.apply_icon_new_game)
        log.debug('__init__.exit')

    def _init_menu_items(self) -> None:
        """Initialize menu related items."""
        self._main_menu_bar: QMenuBar = self.menuBar()
        self._create_game_menu()
        self._create_game_menu_actions()
        self._set_game_menu_action_roles()
        self._set_game_menu_action_texts()
        self._add_game_menu_action_tool_tips()
        self._add_game_menu_action_shortcuts()
        self._game_menu_add_game_menu_actions()
        self._main_menu_bar.addAction(self._game_menu.menuAction())

    def _create_game_menu(self) -> None:
        """Create instance of the QMenu for future use."""
        self._game_menu: QMenu = QMenu(self._main_menu_bar)
        self._game_menu.setTitle('Menu')

    def _create_game_menu_actions(self) -> None:
        """Create actions for the game menu."""
        self._action_new_game: QAction = QAction(self._game_menu)
        self._action_reset_game: QAction = QAction(self._game_menu)
        self._action_exit: QAction = QAction(self._game_menu)

    def _set_game_menu_action_roles(self) -> None:
        """Add roles to the menu actions."""
        self._action_new_game.setMenuRole(
            QAction.MenuRole.ApplicationSpecificRole)
        self._action_reset_game.setMenuRole(
            QAction.MenuRole.ApplicationSpecificRole)
        self._action_exit.setMenuRole(QAction.MenuRole.QuitRole)

    def _set_game_menu_action_texts(self) -> None:
        """Set text for the menu actions."""
        self._action_new_game.setText('New Game')
        self._action_reset_game.setText('Reset Game')
        self._action_exit.setText('Exit')

    def _add_game_menu_action_tool_tips(self) -> None:
        """Set tooltips to the menu actions."""
        self._action_new_game.setToolTip('Start New Game')
        self._action_reset_game.setToolTip(
            'Start New Game with Previous Configuration')
        self._action_exit.setToolTip('Exit From The Game')

    def _add_game_menu_action_shortcuts(self) -> None:
        """Set keyboard shortcuts to the menu actions."""
        self._action_new_game.setShortcut('Ctrl+N')
        self._action_reset_game.setShortcut('Ctrl+R')
        self._action_exit.setShortcut('Ctrl+Q')

    def _game_menu_add_game_menu_actions(self) -> None:
        """Add menu actions to the game menu."""
        self._game_menu.addActions([self._action_new_game,
                                    self._action_reset_game,
                                    self._action_exit])

    def _create_window_container_widget_and_layout(self) -> None:
        """Create main container widget for all child widgets in the app."""
        self._window_container_widget: QWidget = QWidget(self)
        self._window_container_widget_layout: QVBoxLayout = QVBoxLayout(
            self._window_container_widget)
        self._window_container_widget_layout.setContentsMargins(0, 0, 0, 0)
        self._window_container_widget_layout.setSpacing(0)
        self._window_container_widget.setLayout(
            self._window_container_widget_layout)

    def _create_control_widget_container_and_layout(self) -> None:
        """Create and configure main application layout."""
        self._main_control_widget: QWidget = QWidget(
            self._window_container_widget)
        self._main_control_widget_layout: QHBoxLayout = QHBoxLayout(
            self._main_control_widget)
        self._main_control_widget_layout.setContentsMargins(0, 0, 0, 0)
        self._main_control_widget_layout.setSpacing(0)
        self._main_control_widget.setLayout(self._main_control_widget_layout)
        self._main_control_widget.setMaximumHeight(50)

    def _create_control_widgets(self) -> None:
        """Create instances of the control widgets for the main window."""
        self._label_time: QLabel = QLabel(self._main_control_widget)
        self._label_time.setText('Time:')
        self._lcd_time: QLCDNumber = QLCDNumber(self._main_control_widget)
        self._reset_game_push_button: QResetButton = QResetButton(
            self._main_control_widget)
        self._label_flags: QLabel = QLabel(self._main_control_widget)
        self._label_flags.setText('Flags:')
        self._lcd_flags: QLCDNumber = QLCDNumber(self._main_control_widget)

    def _add_control_widgets_to_layout(self) -> None:
        """Add created control widgets to the control widget layout."""
        self._main_control_widget_layout.addWidget(self._label_time)
        self._main_control_widget_layout.addWidget(self._lcd_time)
        self._main_control_widget_layout.addWidget(
            self._reset_game_push_button)
        self._main_control_widget_layout.addWidget(self._label_flags)
        self._main_control_widget_layout.addWidget(self._lcd_flags)

    def _configure_control_widgets(self) -> None:
        """Configure control widgets with default parameters."""
        self._lcd_time.setDecMode()
        self._lcd_time.setDigitCount(10)
        self._lcd_time.display(0)
        self._lcd_flags.setDecMode()
        self._lcd_flags.setDigitCount(10)
        self._lcd_flags.display(0)

    def _add_reset_game_push_button_signal_handler(self) -> None:
        """Connect reset button clicked signal to the handler."""
        self._reset_game_push_button.clicked.connect(
            self._on_reset_game_action_triggered)

    def _add_game_menu_actions_signal_handler(self) -> None:
        """Connect handlers to the signals of the menu actions."""
        self._action_new_game.triggered.connect(
            self._on_new_game_action_triggered)
        self._action_reset_game.triggered.connect(
            self._on_reset_game_action_triggered)
        self._action_exit.triggered.connect(
            self._on_exit_game_action_triggered)

    def _on_new_game_action_triggered(self, checked: bool = False) -> None:
        """Handle on new game action clicked event.

        Args:
            checked (bool, optional): status of the menu action.
                Defaults to False.
        """
        log.debug('checked: %s', checked)
        self._show_new_game_dialog()

    def _on_reset_game_action_triggered(self, checked: bool = False) -> None:
        """Handle on reset game action clicked event.

        Args:
            checked (bool, optional): status of the menu action.
                Defaults to False.
        """
        log.debug('checked: %s', checked)
        instance.CONTROLLER.reset_game()

    def _on_exit_game_action_triggered(self, checked: bool = False) -> None:
        """Handle on exit game action clicked event.

        Args:
            checked (bool, optional): status of the menu action.
                Defaults to False.
        """
        log.debug('checked: %s', checked)
        sys.exit()

    def _show_new_game_dialog(self) -> None:
        """Create and show new game popup dialog."""
        popup: QDialogWidget = QDialogWidget()
        popup_result: int = popup.exec()

        if popup_result:
            number_of_columns: int = popup.number_of_columns
            number_of_rows: int = popup.number_of_rows
            number_of_mines: int = popup.number_of_mines
            config: Configuration = Configuration(
                number_of_rows=number_of_rows,
                number_of_columns=number_of_columns,
                number_of_mines=number_of_mines)
            instance.CONTROLLER.start_new_game(config=config)

    def _on_game_status_update_callback(self,
                                        game_info: GameInformation) -> None:
        """Handle update of the game status.

        Args:
            game_info (GameInformation): game information.
        """
        log.debug('info: %s', game_info)
        if game_info.is_finished and self._timer.isActive():
            self._timer.stop()
        self._lcd_flags.display(game_info.number_of_flags_left)
        self._change_reset_button_icon(game_info)
        if game_info.controller_action in [ControllerActions.NEW_GAME,
                                           ControllerActions.RESET_GAME]:
            self._on_game_update_new_reset(game_info)

    def _change_reset_button_icon(self, game_info: GameInformation) -> None:
        """Change reset button icon based on the vent information.

        Args:
            game_info (GameInformation): game information.
        """
        if game_info.is_finished and game_info.is_player_win:
            self._reset_game_push_button.apply_icon_winner()
        elif game_info.is_finished and not game_info.is_player_win:
            self._reset_game_push_button.apply_icon_exploded()
        else:
            self._reset_game_push_button.apply_icon_new_game()

    def _on_timer_update(self) -> None:
        """Increment time and display it on the lcd widget."""
        self._timer_time += 1
        self._lcd_time.display(self._timer_time)

    def _on_game_update_new_reset(self, game_info: GameInformation) -> None:
        """Reset time value and start timer on the reset or new game event.

        Args:
            game_info (GameInformation): game information.
        """
        self._timer_time = 0
        if not game_info.is_finished and not self._timer.isActive():
            self._timer.start()
