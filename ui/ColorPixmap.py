from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter


class ColorPixmap(QPixmap):
    def __init__(self, source_pixmap, color):
        super().__init__(source_pixmap.size())
        self.fill(Qt.transparent)
        
        painter = QPainter(self)
        painter.drawPixmap(0, 0, source_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(self.rect(), color)
        painter.end()
