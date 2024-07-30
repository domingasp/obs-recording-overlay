from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)
from PySide6.QtCore import Qt

from ui.ui_utilities import load_and_color_icon_pixmap


class IconLabel(QWidget):
    """Displays a text label with an icon on the left."""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.load_icons()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 6)
        layout.setSpacing(14)

        self.icon_label = QLabel()

        self.text_label = QLabel()
        self.text_label.setStyleSheet("color: #ced4da;")
        self.text_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label, stretch=1)

        self.setLayout(layout)

    def load_icons(self):
        """Loads default icons."""
        self.icons = {
            "connected": load_and_color_icon_pixmap(
                icon_path="assets/icons/plug-connected.svg", icon_color="#37b24d"
            ),
            "notConnected": load_and_color_icon_pixmap(
                icon_path="assets/icons/plug-connected-x.svg", icon_color="#f03e3e"
            ),
        }

    def set_connected(self):
        """Updates label to `Connected` and the `connected` icon."""
        self.text_label.setText("Connected")
        self.icon_label.setPixmap(self.icons["connected"])
        self.icon_label.setFixedSize(self.icons["connected"].size())

    def set_not_connected(self):
        """Updates label to `Not Connected` and the `notConnected` icon."""
        self.text_label.setText("Not Connected")
        self.icon_label.setPixmap(self.icons["notConnected"])
        self.icon_label.setFixedSize(self.icons["notConnected"].size())
