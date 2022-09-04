"""Module contains QApplicationMinesweeper class."""
from PyQt6.QtWidgets import QApplication

from minesweeper_ui.widgets.main_window_widget import QMainWindowMinesweeper


class QApplicationMinesweeper(QApplication):
    """Main application class.

    Args:
        QApplication (_type_): parent class.
    """

    def __init__(self) -> None:
        """Initialize application."""
        super().__init__([])
        self._main_widget: QMainWindowMinesweeper = QMainWindowMinesweeper()
        self._main_widget.show()
