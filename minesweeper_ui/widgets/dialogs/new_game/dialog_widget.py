""" """
from PyQt6.QtCore import QRect, QSize
from PyQt6.QtWidgets import QDialog, QVBoxLayout

from minesweeper_ui.widgets.dialogs.new_game.dialog_buttons import \
    QDialogButtons
from minesweeper_ui.widgets.dialogs.new_game.dialog_form import QDialogForm


class QDialogWidget(QDialog):
    """_summary_

    Args:
        QDialog (_type_): _description_
    """

    def __init__(self) -> None:
        """_summary_
        """
        QDialog.__init__(self)
        self.setWindowTitle('Dialog')
        self.setLayout(self._create_layout())
        self.setFixedSize(QSize(380, 190))
        self.layout().addWidget(self._create_form())
        self.layout().addWidget(
            QDialogButtons(dial_accept=self.accept, dial_reject=self.reject))

    def _create_layout(self) -> QVBoxLayout:
        """_summary_

        Returns:
            QVBoxLayout: _description_
        """
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setGeometry(QRect(0, 0, 380, 190))
        return layout

    def _create_form(self) -> QDialogForm:
        """_summary_

        Returns:
            QDialogForm: _description_
        """
        self._form: QDialogForm = QDialogForm()
        return self._form

    @property
    def number_of_rows(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self._form.number_of_rows

    @property
    def number_of_columns(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self._form.number_of_columns

    @property
    def number_of_mines(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        return self._form.number_of_mines
