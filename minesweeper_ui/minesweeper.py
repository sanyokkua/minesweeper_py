"""Main entry point to run QT application."""
import logging

from minesweeper_ui.widgets.application_widget import QApplicationMinesweeper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s %(funcName)s] %(message)s')

log: logging.Logger = logging.getLogger(__name__)


def start_game() -> None:
    """Create instance of the Qt application and run."""
    app: QApplicationMinesweeper = QApplicationMinesweeper()
    app.exec()


if __name__ == '__main__':
    """If the file ran as a script - start the game."""
    start_game()
