""" """
import importlib.resources as res
import logging

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget

import resources

log: logging.Logger = logging.getLogger(__name__)


def load_icon(img_name: str) -> QIcon:
    """_summary_

    Args:
        img_name (str): _description_

    Returns:
        QIcon: _description_
    """
    q_pixmap: QPixmap = load_pixmap(img_name)
    return QIcon(q_pixmap)


def load_pixmap(img_name: str) -> QPixmap:
    """_summary_

    Args:
        img_name (str): _description_

    Returns:
        QPixmap: _description_
    """
    image_png_bytes: bytes = res.read_binary(resources, img_name)
    q_pixmap: QPixmap = QPixmap()
    q_pixmap.loadFromData(image_png_bytes, 'PNG')
    return q_pixmap


def get_smallest_side_size(widget: QWidget) -> int:
    """_summary_

    Args:
        widget (QWidget): _description_

    Returns:
        int: _description_
    """
    log.debug('widget: %s', widget)
    width: int = widget.width()
    height: int = widget.height()
    smallest: int = width if width <= height else height
    log.debug('width: %d, height: %d, smallest: %d', width, height, smallest)
    return smallest
