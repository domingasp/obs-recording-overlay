from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


def image_to_qpixmap(path):
    pixmap = QPixmap(path)
    return pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)


class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        self.load_images()
        self.setup_ui()

    def setup_ui(self):
        self.setup_window()
        self.setup_label()
        self.setup_layout()

    def setup_window(self):
        self.setWindowTitle("overlay")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.WindowTransparentForInput
            | Qt.Tool
        )

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def setup_label(self):
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "background-color: transparent; color: white; padding: 10px;"
        )
        self.label.resize(40, 40)

    def setup_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.setLayout(layout)

    def update_label(self, obs_status):
        icon = "pausedIcon" if obs_status == "paused" else "recordIcon"
        self.label.setPixmap(self.images[icon])

        if obs_status == "stopped":
            self.label.setHidden(True)
        else:
            self.label.setHidden(False)

    def load_images(self):
        self.images = {
            "pausedIcon": image_to_qpixmap("assets/paused-icon.png"),
            "recordIcon": image_to_qpixmap("assets/record-icon.png"),
        }
