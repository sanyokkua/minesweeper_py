"""_summary_
"""
from typing import Callable

from minesweeper_core.api.controller import MinesweeperController
from minesweeper_core.api.dtos import GameInformation

_signal_receivers: set[Callable[[GameInformation], None]] = set()


def subscribe_to_updates(callback: Callable[[GameInformation], None]) -> None:
    """_summary_

    Args:
        callback (Callable[[GameInformation], None]): _description_
    """
    _signal_receivers.add(callback)


def _on_game_status_update_callback(game_info: GameInformation) -> None:
    """_summary_

    Args:
        game_info (GameInformation): _description_
    """
    for callback in _signal_receivers:
        callback(game_info)


CONTROLLER: MinesweeperController = MinesweeperController(
    on_game_status_update_callback=_on_game_status_update_callback)
