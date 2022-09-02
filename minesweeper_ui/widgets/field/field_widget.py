import logging
from typing import Callable

from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QWidget

import minesweeper_ui.game_instance as instance
import minesweeper_ui.widgets.field.utils as utils
from minesweeper_core.api.controller_action_markers import ControllerActionMarkers
from minesweeper_core.api.dtos import GameInformation

log: logging.Logger = logging.getLogger(__name__)


class QWidgetFieldMinesweeper(QWidget):

    def __init__(self) -> None:
        super().__init__()
        log.debug('QWidgetFieldMinesweeper.__init__')
        self._init_widget_layout()
        self._init_field_buttons()
        self._subscribe_to_game_events()
        self._build_mines_field(instance.CONTROLLER.get_game_info())
        self._status_update_handlers: dict[ControllerActionMarkers, Callable[[GameInformation], None]] = {
            ControllerActionMarkers.NEW_GAME: self._build_mines_field,
            ControllerActionMarkers.RESET_GAME: self._reset_field_state,
            ControllerActionMarkers.CELL_OPENED: self._update_mines_field_state,
            ControllerActionMarkers.CELL_FLAGGED: self._update_mines_field_state
        }
        log.debug('QWidgetFieldMinesweeper.__init__.exit')

    def _init_widget_layout(self):
        self._field_grid_layout = QGridLayout()
        self.setLayout(self._field_grid_layout)

    def _init_field_buttons(self):
        self._field_buttons: dict[tuple[int, int], QPushButton] = {}

    def _subscribe_to_game_events(self):
        instance.subscribe_to_updates(self._on_game_status_update_callback)

    def _build_mines_field(self, game_info: GameInformation):
        if game_info is not None:
            self.clear_field()
            field = game_info.game_field.values()
            size_policy: QSizePolicy = QSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )
            size_policy.setHeightForWidth(True)
            size_policy.setWidthForHeight(True)
            for cell in field:
                row_index = cell.row
                col_index = cell.column
                btn: QPushButton = QPushButton()
                btn.setSizePolicy(size_policy)
                btn.setMinimumSize(10, 10)

                def on_click_handler(_checked: bool,
                                     row: int = row_index,
                                     col: int = col_index):
                    # self._on_field_cell_button_clicked(row, col)
                    instance.CONTROLLER.open_cell(row, col)

                utils.apply_push_button_initial_state(btn, cell)

                btn.clicked.connect(on_click_handler)  # TODO: right mouse btn click
                self._field_grid_layout.addWidget(btn, row_index, col_index)
                self._field_grid_layout.setColumnMinimumWidth(col_index, 10)
                self._field_buttons[(row_index, col_index)] = btn

    def clear_field(self) -> None:
        log.debug('QWidgetFieldMinesweeper.clear_field')
        while self.layout().count():
            layout_item = self.layout().takeAt(0)
            if layout_item.widget():
                layout_item.widget().deleteLater()
        self._field_buttons.clear()
        self.layout().update()
        log.debug('QWidgetFieldMinesweeper.clear_field.exit')

    def _on_game_status_update_callback(self, game_info: GameInformation):
        log.debug('_on_game_status_update_callback, game_info: %s', game_info)
        if game_info is not None:
            handler = self._status_update_handlers[game_info.controller_action]
            handler(game_info)

    def _reset_field_state(self, game_info: GameInformation):
        for cell in game_info.game_field.values():
            row_index = cell.row
            col_index = cell.column
            btn = self._field_buttons[(row_index, col_index)]
            utils.apply_push_button_initial_state(btn)

    def _update_mines_field_state(self, game_info):
        if game_info.is_finished:
            for cell in game_info.game_field.values():
                button = self._field_buttons[(cell.row, cell.column)]
                utils.apply_push_button_finish_state(button, cell)
        else:
            for cell in game_info.game_field.values():
                button = self._field_buttons[(cell.row, cell.column)]
                if cell.is_open:
                    utils.apply_push_button_open_state(button, cell)
                elif cell.has_flag:
                    utils.apply_push_button_flag_state(button, cell)
