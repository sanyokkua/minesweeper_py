import logging

from minesweeper_ui.widgets.application_widget import QApplicationMinesweeper

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s [%(name)s %(funcName)s] %(message)s')

log: logging.Logger = logging.getLogger(__name__)


def start_game() -> None:
    app = QApplicationMinesweeper()
    app.exec()


if __name__ == '__main__':
    start_game()
