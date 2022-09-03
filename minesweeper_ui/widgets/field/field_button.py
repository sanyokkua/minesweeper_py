""" """
import enum
import logging
from typing import Callable

from PyQt6.QtCore import QEvent, QSize, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton, QSizePolicy

from minesweeper_core.data.cell import Cell
from minesweeper_ui.utils import get_smallest_side_size, load_icon

log: logging.Logger = logging.getLogger(__name__)


class CellColor(enum.Enum):
    """_summary_

    Args:
        enum (_type_): _description_
    """
    COLOR_BLACK: str = '#000000'
    COLOR_BLUE_50: str = '#e3f2fd'
    COLOR_BLUE_600: str = '#1e88e5'
    COLOR_GREY_400: str = '#bdbdbd'
    COLOR_LIME_300: str = '#dce775'
    COLOR_RED_100: str = '#ffcdd2'
    COLOR_RED_200: str = '#ef9a9a'
    COLOR_RED_300: str = '#e57373'
    COLOR_RED_400: str = '#ef5350'
    COLOR_RED_500: str = '#f44336'
    COLOR_RED_600: str = '#e53935'
    COLOR_RED_700: str = '#d32f2f'
    COLOR_RED_800: str = '#c62828'
    COLOR_WHITE: str = '#ffffff'


class FieldColors(enum.Enum):
    """_summary_

    Args:
        enum (_type_): _description_
    """
    COLOR_INITIAL_STATE: CellColor = CellColor.COLOR_BLUE_600
    COLOR_OPEN_STATE: CellColor = CellColor.COLOR_BLUE_50
    COLOR_FLAG_STATE: CellColor = CellColor.COLOR_LIME_300


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
    CellColor.COLOR_GREY_400: CellColor.COLOR_WHITE,
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


def build_style_by_color(field_color: FieldColors) -> str:
    """_summary_

    Args:
        field_color (FieldColors): _description_

    Returns:
        str: _description_
    """
    log.debug('field_color: %s', field_color.name)
    back_ground_color: CellColor = field_color.value
    log.debug('color: %s', back_ground_color)
    text_color: str = COLOR_TEXT_MAPPING[back_ground_color].value
    style: str = f'background-color: {back_ground_color.value}; border: 1px solid black; color: {text_color}'
    log.debug('style: %s', style)
    return style


def build_style_by_mines(number_of_mines: int) -> str:
    """_summary_

    Args:
        number_of_mines (int): _description_

    Returns:
        str: _description_
    """
    log.debug('number_of_mines: %d', number_of_mines)
    back_ground_color: CellColor = COLOR_TO_MINES_MAPPING[number_of_mines]
    log.debug('color: %s', back_ground_color)
    text_color: str = COLOR_TEXT_MAPPING[back_ground_color].value
    style: str = f'background-color: {back_ground_color.value}; border: 1px solid black; color: {text_color}'
    log.debug('style: %s', style)
    return style


class QFieldButtonCell(QPushButton):
    """_summary_

    Args:
        QPushButton (_type_): _description_
    """

    def __init__(self, cell: Cell,
                 on_mouse_left_button_click: Callable[[Cell], None],
                 on_mouse_right_button_click: Callable[[Cell], None]) -> None:
        """_summary_

        Args:
            cell (Cell): _description_
            on_mouse_left_button_click (Callable[[Cell], None]): _description_
            on_mouse_right_button_click (Callable[[Cell], None]): _description_
        """
        QPushButton.__init__(self)
        self._img_bomb: QIcon = load_icon('bomb.png')
        self._img_flag: QIcon = load_icon('flag.png')
        self._cell: Cell = cell
        self._on_mouse_left_button_click: Callable[
            [Cell], None] = on_mouse_left_button_click
        self._on_mouse_right_button_click: Callable[
            [Cell], None] = on_mouse_right_button_click
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

    def eventFilter(self, obj, event) -> bool:
        """_summary_

        Args:
            obj (_type_): _description_
            event (_type_): _description_

        Returns:
            bool: _description_
        """
        if event.type() == QEvent.Type.MouseButtonPress and obj is self:
            log.debug('QObject: %s, QEvent: %s', obj.__repr__(),
                      event.__repr__())
            if event.button() == Qt.MouseButton.LeftButton:
                log.debug('LeftButton')
                self._on_left_button_press_handler()
            elif event.button() == Qt.MouseButton.RightButton:
                log.debug('RightButton')
                self._on_right_button_press_handler()
            return True
        else:
            return QPushButton.eventFilter(self, obj, event)

    def _on_left_button_press_handler(self) -> None:
        """_summary_
        """
        self._on_mouse_left_button_click(self.cell)

    def _on_right_button_press_handler(self) -> None:
        """_summary_
        """
        self._on_mouse_right_button_click(self.cell)

    def apply_style_initial(self) -> None:
        """_summary_
        """
        self.setEnabled(True)
        self.setChecked(False)
        self.setText('')
        self.setIcon(QIcon())
        self.setStyleSheet(
            build_style_by_color(FieldColors.COLOR_INITIAL_STATE))

    def apply_style_open(self) -> None:
        """_summary_
        """
        self.setEnabled(False)
        self.setChecked(True)
        val: str = f'{self.cell.neighbour_mines}' if self._cell.neighbour_mines > 0 else ''
        self.setText(val)
        self.setStyleSheet(build_style_by_mines(self.cell.neighbour_mines))

    def apply_style_flag(self) -> None:
        """_summary_
        """
        self.setEnabled(True)
        self.setChecked(False)
        self._apply_icon(self._img_flag)
        self.setStyleSheet(build_style_by_color(FieldColors.COLOR_FLAG_STATE))

    def apply_style_finish(self) -> None:
        """_summary_
        """
        self.setChecked(True)
        self.setEnabled(False)
        number_of_mines: str = f'{self.cell.neighbour_mines}' if self.cell.neighbour_mines > 0 else ''
        final_value: str = '' if self.cell.has_mine else number_of_mines
        self.setText(final_value)
        if self.cell.has_mine:
            self.setStyleSheet(
                build_style_by_color(FieldColors.COLOR_OPEN_STATE))
            self._apply_icon(self._img_bomb)
        else:
            self.apply_style_open()

    def _apply_icon(self, icon: QIcon) -> None:
        """_summary_

        Args:
            icon (QIcon): _description_
        """
        self.setIcon(icon)
        smallest_side: int = get_smallest_side_size(self)
        self.setIconSize(QSize(smallest_side, smallest_side))

    @property
    def cell(self) -> Cell:
        """_summary_

        Returns:
            Cell: _description_
        """
        return self._cell

    @cell.setter
    def cell(self, cell: Cell) -> None:
        """_summary_

        Args:
            cell (Cell): _description_
        """
        self._cell = cell
