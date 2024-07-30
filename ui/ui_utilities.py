from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from ui.ColorPixmap import ColorPixmap

def image_to_qpixmap(path):
    pixmap = QPixmap(path)
    return pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)


def load_and_color_icon_pixmap(icon_path, icon_color):
    original_pixmap = QIcon(icon_path).pixmap(QSize(22, 22))
    return ColorPixmap(original_pixmap, icon_color)