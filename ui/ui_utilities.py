from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from ui.ColorPixmap import ColorPixmap


def image_to_qpixmap(path):
    """Loads, scales and returns a QPixmap."""
    pixmap = QPixmap(path)
    return pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)


def load_and_color_icon_pixmap(icon_path, icon_color):
    """Loads and returns a colored image.

    Useful for coloring SVG icons.
    """
    original_pixmap = QIcon(icon_path).pixmap(QSize(22, 22))
    return ColorPixmap(original_pixmap, icon_color)
