"""Module contains QDialogWidget class."""
from PyQt6.QtCore import QRect, QSize
from PyQt6.QtWidgets import QDialog, QVBoxLayout

from minesweeper_ui.widgets.dialogs.new_game.dialog_buttons import \
    QDialogButtons
from minesweeper_ui.widgets.dialogs.new_game.dialog_form import QDialogForm


class QDialogWidget(QDialog):
    """Custom Dialog widget.

    Args:
        QDialog (_type_): parent class.
    """

    def __init__(self) -> None:
        """Initialize dialog widget."""
        QDialog.__init__(self)
        self.setWindowTitle('Select complexity for new game')
        self.setLayout(self._create_layout())
        self.setFixedSize(QSize(380, 190))
        self.layout().addWidget(self._create_form())
        self.layout().addWidget(
            QDialogButtons(dial_accept=self.accept, dial_reject=self.reject))

    def _create_layout(self) -> QVBoxLayout:
        """Create layout of the widget.

        Returns:
            QVBoxLayout: vertical layout.
        """
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setGeometry(QRect(0, 0, 380, 190))
        return layout

    def _create_form(self) -> QDialogForm:
        """Create dialog form.

        Returns:
            QDialogForm: dialog form.
        """
        self._form: QDialogForm = QDialogForm()
        return self._form

    @property
    def number_of_rows(self) -> int:
        """Return number of rows.

        Returns:
            int: number of rows.
        """
        return self._form.number_of_rows

    @property
    def number_of_columns(self) -> int:
        """Return number of columns.

        Returns:
            int: number of columns.
        """
        return self._form.number_of_columns

    @property
    def number_of_mines(self) -> int:
        """Return number of mines.

        Returns:
            int: number of mines.
        """
        return self._form.number_of_mines
