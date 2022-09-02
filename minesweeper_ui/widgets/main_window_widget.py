import logging
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget

import minesweeper_ui.game_instance as instance
from minesweeper_core.api.dtos import GameInformation
from minesweeper_core.constants.default_configurations import BEGINNER
from minesweeper_core.data.field_configuration import Configuration
from minesweeper_ui.widgets.dialogs.new_game.dialog_widget import QDialogWidget
from minesweeper_ui.widgets.field.field_widget import QWidgetFieldMinesweeper

log: logging.Logger = logging.getLogger(__name__)


class QMainWindowMinesweeper(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        log.debug('QMainWindowMinesweeper.__init__')
        self.setWindowTitle('Minesweeper')
        self._field_widget = QWidgetFieldMinesweeper()
        self._init_menu_items()
        self._create_window_container_widget_and_layout()
        self._create_control_widget_container_and_layout()
        self._create_control_widgets()
        self._add_control_widgets_to_layout()
        self._set_control_widgets_texts()
        self._add_reset_game_push_button_signal_handler()
        self._add_game_menu_actions_signal_handler()

        self._window_container_widget_layout.addWidget(self.menuBar())
        self._window_container_widget_layout.addWidget(self._main_control_widget)
        self._window_container_widget_layout.addWidget(self._field_widget)
        self.setCentralWidget(self._window_container_widget)
        min_size = QSize(540, 400)
        self.setMinimumSize(min_size)
        self.resize(min_size)

        instance.subscribe_to_updates(self._on_game_status_update_callback)
        instance.CONTROLLER.start_new_game(BEGINNER)
        log.debug('QMainWindowMinesweeper.__init__.exit')

    def _init_menu_items(self):
        log.debug('_init_menu_items')
        self._main_menu_bar = self.menuBar()
        self._create_game_menu()
        self._create_game_menu_actions()
        self._set_game_menu_action_roles()
        self._set_game_menu_action_texts()
        self._add_game_menu_action_tool_tips()
        self._add_game_menu_action_shortcuts()
        self._game_menu_add_game_menu_actions()
        self._main_menu_bar.addAction(self._game_menu.menuAction())
        # self.setMenuBar(self._main_menu_bar)

    def _create_game_menu(self):
        log.debug('_create_game_menu')
        self._game_menu = QMenu(self._main_menu_bar)
        self._game_menu.setTitle('Menu')

    def _create_game_menu_actions(self):
        log.debug('_create_game_menu_actions')
        self._action_new_game = QAction(self._game_menu)
        self._action_reset_game = QAction(self._game_menu)
        self._action_exit = QAction(self._game_menu)

    def _set_game_menu_action_roles(self):
        log.debug('_set_game_menu_action_roles')
        self._action_new_game.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self._action_reset_game.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
        self._action_exit.setMenuRole(QAction.MenuRole.QuitRole)

    def _set_game_menu_action_texts(self):
        log.debug('_set_game_menu_action_texts')
        self._action_new_game.setText('New Game')
        self._action_reset_game.setText('Reset Game')
        self._action_exit.setText('Exit')

    def _add_game_menu_action_tool_tips(self):
        log.debug('_add_game_menu_action_tool_tips')
        self._action_new_game.setToolTip('Start New Game')
        self._action_reset_game.setToolTip('Start New Game with Previous Configuration')
        self._action_exit.setToolTip('Exit From The Game')

    def _add_game_menu_action_shortcuts(self):
        log.debug('_add_game_menu_action_shortcuts')
        self._action_new_game.setShortcut('Ctrl+N')
        self._action_reset_game.setShortcut('Ctrl+R')
        self._action_exit.setShortcut('Ctrl+Q')

    def _game_menu_add_game_menu_actions(self):
        log.debug('_game_menu_add_game_menu_actions')
        self._game_menu.addActions([self._action_new_game,
                                    self._action_reset_game,
                                    self._action_exit])

    def _create_window_container_widget_and_layout(self):
        log.debug('_create_window_container_widget_and_layout')
        self._window_container_widget = QWidget(self)
        self._window_container_widget_layout = QVBoxLayout(self._window_container_widget)
        self._window_container_widget_layout.setContentsMargins(0, 0, 0, 0)
        self._window_container_widget_layout.setSpacing(0)
        self._window_container_widget.setLayout(self._window_container_widget_layout)

    def _create_control_widget_container_and_layout(self):
        log.debug('_create_control_widget_container_and_layout')
        self._main_control_widget = QWidget(self._window_container_widget)
        self._main_control_widget_layout = QHBoxLayout(self._main_control_widget)
        self._main_control_widget_layout.setContentsMargins(0, 0, 0, 0)
        self._main_control_widget_layout.setSpacing(0)
        self._main_control_widget.setLayout(self._main_control_widget_layout)
        self._main_control_widget.setMaximumHeight(50)

    def _create_control_widgets(self):
        log.debug('_create_control_widgets')
        self._label_time = QLabel(self._main_control_widget)

        expanding_policy = QSizePolicy.Policy.Expanding
        vh_size_policy = QSizePolicy(expanding_policy, expanding_policy)
        self._reset_game_push_button = QPushButton(self._main_control_widget)
        self._reset_game_push_button.setSizePolicy(vh_size_policy)
        self._reset_game_push_button.setMaximumSize(QSize(80, 80))
        self._reset_game_push_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self._label_flags = QLabel(self._main_control_widget)

    def _add_control_widgets_to_layout(self):
        log.debug('_add_control_widgets_to_layout')
        self._main_control_widget_layout.addWidget(self._label_time)
        self._main_control_widget_layout.addWidget(self._reset_game_push_button)
        self._main_control_widget_layout.addWidget(self._label_flags)

    def _set_control_widgets_texts(self):
        log.debug('_set_control_widgets_texts')
        self._label_time.setText('Time')
        self._reset_game_push_button.setText('Reset')
        self._label_flags.setText('Flags:')

    def _add_reset_game_push_button_signal_handler(self):
        log.debug('_add_reset_game_push_button_signal_handler')
        self._reset_game_push_button.clicked.connect(self._on_reset_game_push_button_clicked)

    def _add_game_menu_actions_signal_handler(self):
        log.debug('_add_game_menu_actions_signal_handler')
        self._action_new_game.triggered.connect(self._on_new_game_action_triggered)
        self._action_reset_game.triggered.connect(self._on_reset_game_action_triggered)
        self._action_exit.triggered.connect(self._on_exit_game_action_triggered)

    def _on_reset_game_push_button_clicked(self, checked: bool = False):
        log.debug('_on_reset_game_push_button_clicked, checked: %s', checked)
        instance.CONTROLLER.reset_game()

    def _on_new_game_action_triggered(self, checked: bool = False):
        log.debug('_on_new_game_action_triggered, checked: %s', checked)
        self._show_new_game_dialog()

    def _on_reset_game_action_triggered(self, checked: bool = False):
        log.debug('_on_reset_game_action_triggered, checked: %s', checked)
        instance.CONTROLLER.reset_game()

    def _on_exit_game_action_triggered(self, checked: bool = False):
        log.debug('_on_exit_game_action_triggered, checked: %s', checked)
        sys.exit()

    def _show_new_game_dialog(self):
        log.debug('_show_new_game_dialog')
        popup = QDialogWidget()
        popup_result: int = popup.exec()

        if popup_result:
            number_of_columns = popup.number_of_columns
            number_of_rows = popup.number_of_rows
            number_of_mines = popup.number_of_mines
            config = Configuration(number_of_rows=number_of_rows,
                                   number_of_columns=number_of_columns,
                                   number_of_mines=number_of_mines)
            instance.CONTROLLER.start_new_game(config=config)

    def _on_game_status_update_callback(self, game_info: GameInformation):
        log.debug('_on_game_status_update_callback, info: %s', game_info)
        self._label_flags.setText(str(game_info.number_of_flags_left))
