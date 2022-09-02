import logging
from typing import Callable

from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QWidget

import minesweeper_ui.game_instance as instance
from minesweeper_core.api.controller_action_markers import ControllerActionMarkers
from minesweeper_core.api.dtos import GameInformation
from minesweeper_core.data.cell import Cell
from minesweeper_ui.widgets.field.field_button import QFieldButtonCell

log: logging.Logger = logging.getLogger(__name__)


class QWidgetFieldMinesweeper(QWidget):

    def __init__(self) -> None:
        super().__init__()
        log.debug('start')
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
        log.debug('end')

    def _init_widget_layout(self):
        self._field_grid_layout = QGridLayout()
        self._field_grid_layout.setContentsMargins(0, 0, 0, 0)
        self._field_grid_layout.setSpacing(0)
        self.setLayout(self._field_grid_layout)

    def _init_field_buttons(self):
        self._field_buttons: dict[tuple[int, int], QFieldButtonCell] = {}

    def _subscribe_to_game_events(self):
        instance.subscribe_to_updates(self._on_game_status_update_callback)

    def _build_mines_field(self, game_info: GameInformation):
        if game_info is not None:
            self.clear_field()
            field = game_info.game_field.values()
            for cell in field:
                row_index = cell.row
                col_index = cell.column
                btn: QFieldButtonCell = QFieldButtonCell(
                    cell=cell,
                    on_mouse_left_button_click=self._on_mouse_left_button_click,
                    on_mouse_right_button_click=self._on_mouse_right_button_click
                )
                btn.apply_style_initial()
                self._field_grid_layout.addWidget(btn, row_index, col_index)
                self._field_grid_layout.setColumnMinimumWidth(col_index, 10)
                self._field_buttons[(row_index, col_index)] = btn

    def clear_field(self) -> None:
        while self.layout().count():
            layout_item = self.layout().takeAt(0)
            if layout_item.widget():
                layout_item.widget().deleteLater()
        self._field_buttons.clear()
        self.layout().update()

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
            btn.cell = cell
            btn.apply_style_initial()

    def _update_mines_field_state(self, game_info):
        for cell in game_info.game_field.values():
            button = self._field_buttons[(cell.row, cell.column)]
            button.apply_style_initial()
            if game_info.is_finished:
                button.apply_style_finish()
            elif cell.is_open:
                button.apply_style_open()
            elif cell.has_flag:
                button.apply_style_flag()

    def _on_mouse_left_button_click(self, cell: Cell):
        instance.CONTROLLER.open_cell(cell.row, cell.column)

    def _on_mouse_right_button_click(self, cell: Cell):
        instance.CONTROLLER.flag_cell(cell.row, cell.column)
