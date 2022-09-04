"""Module contains custom buttons classes."""
from PyQt6.QtCore import QEvent, QSize, Qt
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import QPushButton, QSizePolicy

from minesweeper_ui.utils import get_smallest_side_size, load_icon


class QResetButton(QPushButton):
    """Custom implementation of the QPushButton.

    Represent functionality required for the Game Reset Button.

    Args:
        QPushButton (_type_): parent class.
    """

    def __init__(self, parent) -> None:
        """Initialize button.

        Args:
            parent (_type_): parent widget (container).
        """
        QPushButton.__init__(self, parent)
        self._img_new_game: QIcon = load_icon('new_game.png')
        self._img_exploded: QIcon = load_icon('exploded.png')
        self._img_winner: QIcon = load_icon('winner.png')
        self._img_wink: QIcon = load_icon('wink.png')
        self._current_icon: QIcon = self._img_new_game

        expanding_policy: QSizePolicy.Policy = QSizePolicy.Policy.Expanding
        vh_size_policy: QSizePolicy = QSizePolicy(expanding_policy,
                                                  expanding_policy)
        self.setSizePolicy(vh_size_policy)
        self.setMaximumSize(QSize(80, 80))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.installEventFilter(self)
        self.apply_icon_new_game()

    def eventFilter(self, obj, event) -> bool:
        """Override eventFilter functionality.

        Adds implementation for the hover event above reset button to
        change icon.

        Args:
            obj (_type_): source object that sends event.
            event (_type_): event that was generated.

        Returns:
            bool: status of the processed event.
        """
        if event.type() == QEvent.Type.Enter and obj is self:
            self._apply_icon_wink()
            return True
        elif event.type() == QEvent.Type.Leave:
            self._previous_icon()
            return True
        else:
            return QPushButton.eventFilter(self, obj, event)

    def _apply_icon_wink(self) -> None:
        """Change current icon to the wink smile."""
        self._apply_icon(self._img_wink)

    def _previous_icon(self) -> None:
        """Change current icon to the previous."""
        self._apply_icon(self._current_icon)

    def _apply_icon(self, icon: QIcon) -> None:
        """Change current icon to the passed icon.

        Args:
            icon (QIcon): icon that should be applied.
        """
        self.setIcon(icon)
        smallest_side: int = get_smallest_side_size(self)
        self.setStyleSheet('border : 0; background: transparent;')
        self.setIconSize(QSize(smallest_side, smallest_side))

    def apply_icon_new_game(self) -> None:
        """Change current icon to the new game icon."""
        self._current_icon = self._img_new_game
        self._apply_icon(self._img_new_game)

    def apply_icon_winner(self) -> None:
        """Change current icon to the winner icon."""
        self._current_icon = self._img_winner
        self._apply_icon(self._img_winner)

    def apply_icon_exploded(self) -> None:
        """Change current icon to the exploded icon."""
        self._current_icon = self._img_exploded
        self._apply_icon(self._img_exploded)
