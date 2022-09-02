import logging

from PyQt6.QtCore import QRect
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QVBoxLayout

from minesweeper_ui.widgets.dialogs.new_game.dialog_buttons import QDialogButtons
from minesweeper_ui.widgets.dialogs.new_game.dialog_form import QDialogForm

log: logging.Logger = logging.getLogger(__name__)


class QDialogWidget(QDialog):
    def __init__(self) -> None:
        QDialog.__init__(self)
        log.debug('__init__ of QDialogWidget')
        self.setWindowTitle('Dialog')
        self.setLayout(self._create_layout())
        self.setFixedSize(QSize(380, 190))
        self.layout().addWidget(self._create_form())
        self.layout().addWidget(QDialogButtons(dial_accept=self.accept, dial_reject=self.reject))

    def _create_layout(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setGeometry(QRect(0, 0, 380, 190))
        return layout

    def _create_form(self):
        self._form = QDialogForm()
        return self._form

    @property
    def number_of_rows(self) -> int:
        return self._form.number_of_rows

    @property
    def number_of_columns(self) -> int:
        return self._form.number_of_columns

    @property
    def number_of_mines(self) -> int:
        return self._form.number_of_mines
