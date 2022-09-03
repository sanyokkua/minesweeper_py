""" """
from PyQt6.QtWidgets import QApplication

from minesweeper_ui.widgets.main_window_widget import QMainWindowMinesweeper


class QApplicationMinesweeper(QApplication):
    """_summary_

    Args:
        QApplication (_type_): _description_
    """

    def __init__(self) -> None:
        """_summary_
        """
        super().__init__([])
        self._main_control_widget: QMainWindowMinesweeper = QMainWindowMinesweeper()
        self._main_control_widget.show()
