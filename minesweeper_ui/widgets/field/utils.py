import logging

from PyQt6.QtWidgets import QPushButton

from minesweeper_core.data.cell import Cell

log: logging.Logger = logging.getLogger(__name__)


def apply_push_button_initial_state(button: QPushButton, cell: Cell | None = None):
    log.debug('apply_push_button_initial_state. btn: %s, cell: %s', button, cell)
    button.setEnabled(True)
    button.setChecked(False)
    button.setText('')


def apply_push_button_open_state(button: QPushButton, cell: Cell):
    log.debug('apply_push_button_open_state. btn: %s, cell: %s', button, cell)
    button.setEnabled(False)
    button.setChecked(True)
    val = f'{cell.neighbour_mines}' if cell.neighbour_mines > 0 else ''
    button.setText(val)


def apply_push_button_flag_state(button: QPushButton, cell: Cell | None = None):
    log.debug('apply_push_button_flag_state. btn: %s, cell: %s', button, cell)
    button.setEnabled(True)
    button.setChecked(False)
    button.setText('F')


def apply_push_button_finish_state(button: QPushButton, cell: Cell):
    log.debug('apply_push_button_finish_state. btn: %s, cell: %s', button, cell)
    button.setChecked(True)
    button.setEnabled(False)
    number_of_mines = f'{cell.neighbour_mines}' if cell.neighbour_mines > 0 else ''
    final_value = '*' if cell.has_mine else number_of_mines
    button.setText(final_value)
