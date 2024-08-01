from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QSystemTrayIcon,
    QMenu,
    QWidgetAction,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction

from ui.ConnectionSetupWindow import ConnectionSetupWindow
from ui.IconLabel import IconLabel
from ui.ui_utilities import image_to_qpixmap


class Overlay(QWidget):
    """Top most window overlay with clickthrough capabilities. Includes system tray."""

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
        """Initialised overlay window by setting relevant Window flags and a title."""
        self.setWindowTitle("OBS Recording Overlay")
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
            | Qt.FramelessWindowHint
            | Qt.WindowTransparentForInput
            | Qt.Tool
        )

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def setup_label(self):
        """Initialises overlay label."""
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: transparent; padding: 10px;")
        self.label.resize(40, 40)

    def setup_layout(self):
        """Initialised layout with bottom-left alignment."""
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignBottom | Qt.AlignLeft)
        self.setLayout(layout)

    def setup_tray(self):
        """Initialises system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("assets/obs-recording-overlay-logo.png"))
        self.tray_icon.setToolTip("OBS Recording Overlay")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)

        self.connection_status_icon_label = IconLabel()
        self.connection_status_icon_label.set_not_connected()
        connected_state_action = QWidgetAction(self)
        connected_state_action.setDefaultWidget(self.connection_status_icon_label)

        connection_setup_action = QAction("Configure Connection", self)
        connection_setup_action.triggered.connect(self.show_connection_setup)

        tray_menu = QMenu(self)

        tray_menu.addAction(connected_state_action)
        tray_menu.addSeparator()
        tray_menu.addAction(connection_setup_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def update_label(self, obs_status):
        """Updates overlay image. Hides label if not recording."""
        icon = "pausedIcon" if obs_status == "paused" else "recordIcon"
        self.label.setPixmap(self.images[icon])

        if obs_status == "stopped":
            self.label.setHidden(True)
        else:
            self.label.setHidden(False)

    def update_connected(self, is_connected):
        """Updates connected status icon and label according to `is_connected`."""
        if is_connected:
            self.connection_status_icon_label.set_connected()
        else:
            self.connection_status_icon_label.set_not_connected()

    def load_images(self):
        """Loads the default overlay images."""
        self.images = {
            "pausedIcon": image_to_qpixmap("assets/paused-icon.png"),
            "recordIcon": image_to_qpixmap("assets/record-icon.png"),
        }

    def show_connection_setup(self):
        connection_setup_window = ConnectionSetupWindow()
        connection_setup_window.exec_()
