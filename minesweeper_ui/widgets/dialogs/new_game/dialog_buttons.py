import logging

from PyQt6.QtWidgets import QDialogButtonBox

log: logging.Logger = logging.getLogger(__name__)


class QDialogButtons(QDialogButtonBox):
    def __init__(self, dial_accept, dial_reject) -> None:
        QDialogButtonBox.__init__(self)

        button_cancel = QDialogButtonBox.StandardButton.Cancel
        button_ok = QDialogButtonBox.StandardButton.Ok
        dialog_buttons = button_cancel | button_ok

        self.setStandardButtons(dialog_buttons)
        self.accepted.connect(dial_accept)
        self.rejected.connect(dial_reject)
