"""Module contains QDialogButtons class."""
import logging

from PyQt6.QtWidgets import QDialogButtonBox

log: logging.Logger = logging.getLogger(__name__)


class QDialogButtons(QDialogButtonBox):
    """Define Dialog buttons box that is used for new game dialog.

    Args:
        QDialogButtonBox (_type_): parent class.
    """

    def __init__(self, dial_accept, dial_reject) -> None:
        """Initialize widget.

        Args:
            dial_accept (_type_): dialog accept handler.
            dial_reject (_type_): dialog reject handler.
        """
        QDialogButtonBox.__init__(self)

        cancel = QDialogButtonBox.StandardButton.Cancel
        button_cancel: QDialogButtonBox.StandardButton = cancel
        ok = QDialogButtonBox.StandardButton.Ok
        button_ok: QDialogButtonBox.StandardButton = ok
        dialog_buttons = button_cancel | button_ok

        self.setStandardButtons(dialog_buttons)
        self.accepted.connect(dial_accept)
        self.rejected.connect(dial_reject)
