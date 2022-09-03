""" """
import logging

from PyQt6.QtWidgets import QDialogButtonBox

log: logging.Logger = logging.getLogger(__name__)


class QDialogButtons(QDialogButtonBox):
    """_summary_

    Args:
        QDialogButtonBox (_type_): _description_
    """

    def __init__(self, dial_accept, dial_reject) -> None:
        """_summary_

        Args:
            dial_accept (_type_): _description_
            dial_reject (_type_): _description_
        """
        QDialogButtonBox.__init__(self)

        button_cancel: QDialogButtonBox.StandardButton = QDialogButtonBox.StandardButton.Cancel
        button_ok: QDialogButtonBox.StandardButton = QDialogButtonBox.StandardButton.Ok
        dialog_buttons = button_cancel | button_ok

        self.setStandardButtons(dialog_buttons)
        self.accepted.connect(dial_accept)
        self.rejected.connect(dial_reject)
