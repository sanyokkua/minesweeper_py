"""Util methods that are used in the qt application."""
import importlib.resources as res
import logging

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget

import resources

log: logging.Logger = logging.getLogger(__name__)


def load_icon(img_name: str) -> QIcon:
    """Load image and return built QIcon on this image.

    Args:
        img_name (str): name of the image that should be loaded.

    Returns:
        QIcon: Built QIcon from loaded image
    """
    q_pixmap: QPixmap = load_pixmap(img_name)
    return QIcon(q_pixmap)


def load_pixmap(img_name: str) -> QPixmap:
    """Load and build QPixmap from the image.

    Args:
        img_name (str): name of the image that should be loaded.

    Returns:
        QPixmap: pixmap that is built from image.
    """
    image_png_bytes: bytes = res.read_binary(resources, img_name)
    q_pixmap: QPixmap = QPixmap()
    q_pixmap.loadFromData(image_png_bytes, 'PNG')
    return q_pixmap


def get_smallest_side_size(widget: QWidget) -> int:
    """Calculate the smallest side of the widget.

    Widget has width and height dimensions, and this function will find
    what dimension is the smallest and return or original width, or
    original height, depends on what is smaller.

    Args:
        widget (QWidget): QWidget and its children classes.

    Returns:
        int: smallest dimension (size).
    """
    log.debug('widget: %s', widget)
    width: int = widget.width()
    height: int = widget.height()
    smallest: int = width if width <= height else height
    log.debug('width: %d, height: %d, smallest: %d', width, height, smallest)
    return smallest
