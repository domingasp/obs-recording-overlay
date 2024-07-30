from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QPixmap, QIcon, QAction


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
        self.setup_tray()

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
            "background-color: transparent; padding: 10px;"
        )
        self.label.resize(40, 40)

    def setup_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.setLayout(layout)

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('assets/obs-recording-overlay-logo.png'))
        self.tray_icon.setToolTip('OBS Recording Overlay')

        tray_menu = QMenu(self)
        tray_menu.setStyleSheet("""
            QMenu {
                padding: 2px;
                background-color: #2C2E33;
                min-width: 50px;
            }
            QMenu::item {
                padding: 4px 12px;
                font-size: 13px;
                width: 100%;
                border-radius: 4px;
                line-height: 15px;
            }
            QMenu::item:selected {
                background-color: #f03e3e;
            }
        """)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

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
