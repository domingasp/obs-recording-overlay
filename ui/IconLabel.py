from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)

from ui.ui_utilities import load_and_color_icon_pixmap


class IconLabel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.load_icons()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 6)
        layout.setSpacing(0)

        self.icon_label = QLabel()

        self.text_label = QLabel()
        self.text_label.setStyleSheet("color: #ced4da;")

        layout.addWidget(self.text_label)
        layout.addWidget(self.icon_label)

        self.setLayout(layout)

    def load_icons(self):
        self.icons = {
            "connected": load_and_color_icon_pixmap(
                icon_path="assets/icons/plug-connected.svg", icon_color="#37b24d"
            ),
            "notConnected": load_and_color_icon_pixmap(
                icon_path="assets/icons/plug-connected-x.svg", icon_color="#f03e3e"
            ),
        }

    def set_connected(self):
        self.text_label.setText("Connected")
        self.icon_label.setPixmap(self.icons["connected"])
        self.icon_label.setFixedSize(self.icons["connected"].size())

    def set_not_connected(self):
        self.text_label.setText("Not Connected")
        self.icon_label.setPixmap(self.icons["notConnected"])
        self.icon_label.setFixedSize(self.icons["notConnected"].size())
