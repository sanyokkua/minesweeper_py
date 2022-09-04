"""Represent game instance objects."""
from typing import Callable

from minesweeper_core.api.controller import MinesweeperController
from minesweeper_core.api.dtos import GameInformation

_signal_receivers: set[Callable[[GameInformation], None]] = set()


def subscribe_to_updates(callback: Callable[[GameInformation], None]) -> None:
    """Add to the signal receivers list new receiver.

    Args:
        callback (Callable[[GameInformation], None]): callback function
            that will be called on the changes in the controller game
            state.
    """
    _signal_receivers.add(callback)


def _on_game_status_update_callback(game_info: GameInformation) -> None:
    """Send notification about updates to all receivers.

    Args:
        game_info (GameInformation): game information.
    """
    for callback in _signal_receivers:
        callback(game_info)


# Instance of the controller that will be used for application instance
CONTROLLER: MinesweeperController = MinesweeperController(
    on_game_status_update_callback=_on_game_status_update_callback)
