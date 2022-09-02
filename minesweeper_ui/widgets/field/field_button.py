import enum
import logging

from PyQt6.QtCore import QEvent
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSizePolicy

from minesweeper_core.data.cell import Cell
from minesweeper_ui.utils import load_icon

log: logging.Logger = logging.getLogger(__name__)


class CellColor(enum.Enum):
    COLOR_BLACK = '#000000'
    COLOR_BLUE_50 = '#e3f2fd'
    COLOR_BLUE_600 = '#1e88e5'
    COLOR_BLUE_GREY_900 = '#263238'
    COLOR_LIME_300 = '#dce775'
    COLOR_RED_100 = '#ffcdd2'
    COLOR_RED_200 = '#ef9a9a'
    COLOR_RED_300 = '#e57373'
    COLOR_RED_400 = '#ef5350'
    COLOR_RED_500 = '#f44336'
    COLOR_RED_600 = '#e53935'
    COLOR_RED_700 = '#d32f2f'
    COLOR_RED_800 = '#c62828'
    COLOR_WHITE = '#ffffff'


class FieldColors(enum.Enum):
    COLOR_INITIAL_STATE = CellColor.COLOR_BLUE_600
    COLOR_OPEN_STATE = CellColor.COLOR_BLUE_50
    COLOR_FLAG_STATE = CellColor.COLOR_LIME_300
    COLOR_MINE_STATE = CellColor.COLOR_BLUE_GREY_900


COLOR_TO_MINES_MAPPING: dict[int, CellColor] = {
    0: CellColor.COLOR_BLUE_50,
    1: CellColor.COLOR_RED_100,
    2: CellColor.COLOR_RED_200,
    3: CellColor.COLOR_RED_300,
    4: CellColor.COLOR_RED_400,
    5: CellColor.COLOR_RED_500,
    6: CellColor.COLOR_RED_600,
    7: CellColor.COLOR_RED_700,
    8: CellColor.COLOR_RED_800
}

COLOR_TEXT_MAPPING: dict[CellColor, CellColor] = {
    CellColor.COLOR_BLACK: CellColor.COLOR_WHITE,
    CellColor.COLOR_BLUE_50: CellColor.COLOR_BLACK,
    CellColor.COLOR_BLUE_600: CellColor.COLOR_BLACK,
    CellColor.COLOR_BLUE_GREY_900: CellColor.COLOR_WHITE,
    CellColor.COLOR_LIME_300: CellColor.COLOR_BLACK,
    CellColor.COLOR_RED_100: CellColor.COLOR_BLACK,
    CellColor.COLOR_RED_200: CellColor.COLOR_BLACK,
    CellColor.COLOR_RED_300: CellColor.COLOR_BLACK,
    CellColor.COLOR_RED_400: CellColor.COLOR_BLACK,
    CellColor.COLOR_RED_500: CellColor.COLOR_BLACK,
    CellColor.COLOR_RED_600: CellColor.COLOR_WHITE,
    CellColor.COLOR_RED_700: CellColor.COLOR_WHITE,
    CellColor.COLOR_RED_800: CellColor.COLOR_WHITE,
    CellColor.COLOR_WHITE: CellColor.COLOR_BLACK
}


def build_style_by_color(field_color: FieldColors):
    log.debug('field_color: %s', field_color.name)
    back_ground_color = field_color.value
    log.debug('color: %s', back_ground_color)
    text_color = COLOR_TEXT_MAPPING[back_ground_color].value
    style: str = f'background-color: {back_ground_color.value}; border: 1px solid black; color: {text_color}'
    log.debug('style: %s', style)
    return style


def build_style_by_mines(number_of_mines: int):
    log.debug('number_of_mines: %d', number_of_mines)
    back_ground_color = COLOR_TO_MINES_MAPPING[number_of_mines]
    log.debug('color: %s', back_ground_color)
    text_color = COLOR_TEXT_MAPPING[back_ground_color].value
    style: str = f'background-color: {back_ground_color.value}; border: 1px solid black; color: {text_color}'
    log.debug('style: %s', style)
    return style


class QFieldButtonCell(QPushButton):
    def __init__(self, cell: Cell,
                 on_mouse_left_button_click,
                 on_mouse_right_button_click):
        QPushButton.__init__(self)
        self._img_bomb = load_icon('bomb.png')
        self._cell = cell
        self._on_mouse_left_button_click = on_mouse_left_button_click
        self._on_mouse_right_button_click = on_mouse_right_button_click
        size_policy: QSizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        size_policy.setHeightForWidth(True)
        size_policy.setWidthForHeight(True)
        self.setSizePolicy(size_policy)
        self.setMinimumSize(10, 10)
        self.apply_style_initial()
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseButtonPress and obj is self:
            log.debug('QObject: %s, QEvent: %s', obj.__repr__(), event.__repr__())
            if event.button() == Qt.MouseButton.LeftButton:
                log.debug('LeftButton')
                self._on_left_button_press_handler()
            elif event.button() == Qt.MouseButton.RightButton:
                log.debug('RightButton')
                self._on_right_button_press_handler()
            return True
        else:
            return QPushButton.eventFilter(self, obj, event)

    def _on_left_button_press_handler(self):
        self._on_mouse_left_button_click(self.cell)

    def _on_right_button_press_handler(self):
        self._on_mouse_right_button_click(self.cell)

    def apply_style_initial(self):
        self.setEnabled(True)
        self.setChecked(False)
        self.setText('')
        self.setIcon(QIcon())
        self.setStyleSheet(build_style_by_color(FieldColors.COLOR_INITIAL_STATE))

    def apply_style_open(self):
        self.setEnabled(False)
        self.setChecked(True)
        val = f'{self.cell.neighbour_mines}' if self._cell.neighbour_mines > 0 else ''
        self.setText(val)
        self.setStyleSheet(build_style_by_mines(self.cell.neighbour_mines))

    def apply_style_flag(self):
        self.setEnabled(True)
        self.setChecked(False)
        self.setText('F')
        self.setStyleSheet(build_style_by_color(FieldColors.COLOR_FLAG_STATE))

    def apply_style_finish(self):
        self.setChecked(True)
        self.setEnabled(False)
        number_of_mines = f'{self.cell.neighbour_mines}' if self.cell.neighbour_mines > 0 else ''
        final_value = '*' if self.cell.has_mine else number_of_mines
        self.setText(final_value)
        if self.cell.has_mine:
            self.setStyleSheet(build_style_by_color(FieldColors.COLOR_MINE_STATE))
            self.setIcon(self._img_bomb)
        else:
            self.apply_style_open()

    @property
    def cell(self):
        return self._cell

    @cell.setter
    def cell(self, cell: Cell):
        self._cell = cell
