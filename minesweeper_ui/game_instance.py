from typing import Callable

from minesweeper_core.api.controller import MinesweeperController
from minesweeper_core.api.dtos import GameInformation

_signal_receivers: set[Callable[[GameInformation], None]] = set()


def subscribe_to_updates(callback: Callable[[GameInformation], None]):
    _signal_receivers.add(callback)


def _on_game_status_update_callback(game_info: GameInformation):
    for callback in _signal_receivers:
        callback(game_info)


CONTROLLER = MinesweeperController(on_game_status_update_callback=_on_game_status_update_callback)
