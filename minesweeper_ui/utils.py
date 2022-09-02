import importlib.resources as res

from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap

import resources


def load_icon(img_name: str) -> QIcon:
    image_png_bytes: bytes = res.read_binary(resources, img_name)
    q_pixmap = QPixmap()
    q_pixmap.loadFromData(image_png_bytes, 'PNG')
    return QIcon(q_pixmap)
