from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer


def create_colored_icon(svg_path: str, color_hex: str, size=(64, 64)) -> QIcon:
    color = QColor(color_hex)
    renderer = QSvgRenderer(svg_path)
    pixmap = QPixmap(size[0], size[1])
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)

    painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()

    return QIcon(pixmap)
