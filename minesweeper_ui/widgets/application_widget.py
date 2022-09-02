import logging

from PyQt6.QtWidgets import QApplication

from minesweeper_ui.widgets.main_window_widget import QMainWindowMinesweeper

log: logging.Logger = logging.getLogger(__name__)


class QApplicationMinesweeper(QApplication):

    def __init__(self) -> None:
        super().__init__([])
        log.debug('QApplicationMinesweeper.__init__')
        self._main_control_widget = QMainWindowMinesweeper()
        self._main_control_widget.show()
        log.debug('QApplicationMinesweeper.__init__.exit')
