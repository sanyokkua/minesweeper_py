"""Module contains QFieldButtonCell class and helper class and variables."""
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
    """Represent available colors that are used in the game.

    Args:
        enum.Enum (_type_): parent class.
    """

    COLOR_BLACK = '#000000'
    COLOR_BLUE_50 = '#e3f2fd'
    COLOR_BLUE_600 = '#1e88e5'
    COLOR_GREY_400 = '#bdbdbd'
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
    """Represent default colors for the game states.

    Args:
        enum.Enum (_type_): parent class.
    """

    COLOR_INITIAL_STATE = CellColor.COLOR_BLUE_600
    COLOR_OPEN_STATE = CellColor.COLOR_BLUE_50
    COLOR_FLAG_STATE = CellColor.COLOR_LIME_300


# Mapping of the number of mines to the color of the cell.
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

# Mapping of the background color to the foreground text colors.
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
    """Build string style for the passed field_color.

    Args:
        field_color (FieldColors): field color.

    Returns:
        str: style string.
    """
    log.debug('field_color: %s', field_color.name)
    back_ground_color: CellColor = field_color.value
    return build_style(back_ground_color)


def build_style_by_mines(number_of_mines: int) -> str:
    """Build string style for the passed number of mines.

    Args:
        number_of_mines (int): number of mines around the cell. 0-8

    Returns:
        str: style string.
    """
    log.debug('number_of_mines: %d', number_of_mines)
    back_ground_color: CellColor = COLOR_TO_MINES_MAPPING[number_of_mines]
    return build_style(back_ground_color)


def build_style(back_ground_color: CellColor) -> str:
    """Build string style for the passed background color.

    Args:
        back_ground_color (CellColor): background color.

    Returns:
        str: style string.
    """
    log.debug('color: %s', back_ground_color)
    text_color: str = COLOR_TEXT_MAPPING[back_ground_color].value
    background: str = f'background-color: {back_ground_color.value};'
    border: str = 'border: 1px solid black;'
    color: str = f'color: {text_color}'
    style: str = ' '.join([background, border, color])
    log.debug('style: %s', style)
    return style


class QFieldButtonCell(QPushButton):
    """Custom button to represent Field Cell.

    Args:
        QPushButton (_type_): parent class.
    """

    def __init__(self, cell: Cell,
                 on_mouse_left_button_click: Callable[[Cell], None],
                 on_mouse_right_button_click: Callable[[Cell], None]) -> None:
        """Initialize button.

        Args:
            cell (Cell): instance of the related cell.
            on_mouse_left_button_click (Callable[[Cell], None]):
                handler of the left mouse button click
            on_mouse_right_button_click (Callable[[Cell], None]):
                handler of the right mouse button click
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
        """Override eventFilter functionality.

        Adds implementation for the left/right mouse button click
        events.

        Args:
            obj (_type_): source object that sends event.
            event (_type_): event that was generated.

        Returns:
            bool: status of the processed event.
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
        """Handle left mouse button click event."""
        self._on_mouse_left_button_click(self.cell)

    def _on_right_button_press_handler(self) -> None:
        """Handle right mouse button click event."""
        self._on_mouse_right_button_click(self.cell)

    def apply_style_initial(self) -> None:
        """Change button state that should be initial after game starts."""
        self.setEnabled(True)
        self.setChecked(False)
        self.setText('')
        self.setIcon(QIcon())
        self.setStyleSheet(
            build_style_by_color(FieldColors.COLOR_INITIAL_STATE))

    def apply_style_open(self) -> None:
        """Change button state that should be in open cell."""
        self.setEnabled(False)
        self.setChecked(True)
        mines = self._cell.neighbour_mines
        val: str = f'{mines}' if mines > 0 else ''
        self.setText(val)
        self.setStyleSheet(build_style_by_mines(self.cell.neighbour_mines))

    def apply_style_flag(self) -> None:
        """Change button state that should be in flagged cell."""
        self.setEnabled(True)
        self.setChecked(False)
        self._apply_icon(self._img_flag)
        self.setStyleSheet(build_style_by_color(FieldColors.COLOR_FLAG_STATE))

    def apply_style_finish(self) -> None:
        """Change button state that should be when game is finished."""
        self.setChecked(True)
        self.setEnabled(False)
        mines = self.cell.neighbour_mines
        number_of_mines: str = f'{mines}' if mines > 0 else ''
        final_value: str = '' if self.cell.has_mine else number_of_mines
        self.setText(final_value)
        if self.cell.has_mine:
            self.setStyleSheet(
                build_style_by_color(FieldColors.COLOR_OPEN_STATE))
            self._apply_icon(self._img_bomb)
        else:
            self.apply_style_open()

    def _apply_icon(self, icon: QIcon) -> None:
        """Change icon to the passed.

        Args:
            icon (QIcon): icon.
        """
        self.setIcon(icon)
        smallest_side: int = get_smallest_side_size(self)
        self.setIconSize(QSize(smallest_side, smallest_side))

    @property
    def cell(self) -> Cell:
        """Return related cell.

        Returns:
            Cell: cell
        """
        return self._cell

    @cell.setter
    def cell(self, cell: Cell) -> None:
        """Set related cell for this button.

        Args:
            cell (Cell): cell.
        """
        self._cell = cell
