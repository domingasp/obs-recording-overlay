from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QSystemTrayIcon,
    QMenu,
    QWidgetAction,
)
from PySide6.QtCore import Qt, Slot, QSettings
from PySide6.QtGui import QIcon, QAction

from ui.__ConnectionSetupWindow import ConnectionSetupWindow
from ui.__IconLabel import IconLabel
from ui.__ui_utilities import image_to_qpixmap


class Overlay(QWidget):
    """Top most window overlay with clickthrough capabilities. Includes system tray."""

    def __init__(self):
        super().__init__()
        self.websocket_client = None

        self.settings = QSettings("Lemtale", "OBS Recording Overlay")

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
        self.overlay_label = QLabel()
        self.overlay_label.setAlignment(Qt.AlignCenter)
        self.overlay_label.setStyleSheet(
            "background-color: transparent; padding: 10px;"
        )
        self.overlay_label.resize(40, 40)

    def setup_layout(self):
        """Initialised layout with bottom-left alignment."""
        layout = QVBoxLayout()
        layout.addWidget(self.overlay_label)
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
        self.overlay_label.setPixmap(self.images[icon])

        if obs_status == "stopped":
            self.overlay_label.setHidden(True)
        else:
            self.overlay_label.setHidden(False)

    def update_connected(self, is_connected):
        """Updates connected status icon and label according to `is_connected`."""
        if is_connected:
            self.connection_status_icon_label.set_connected()
        else:
            self.connection_status_icon_label.set_not_connected()
            self.overlay_label.setHidden(True)

    def load_images(self):
        """Loads the default overlay images."""
        self.images = {
            "pausedIcon": image_to_qpixmap("assets/paused-icon.png"),
            "recordIcon": image_to_qpixmap("assets/record-icon.png"),
        }

    def set_websocket_client(self, websocket_client):
        self.websocket_client = websocket_client
        self.update_websocket_client_connection_details()

    def save_settings(self, url, port, password):
        self.settings.setValue("websocket_url", url)
        self.settings.setValue("websocket_port", port)
        self.settings.setValue("websocket_password", password)
        self.update_websocket_client_connection_details()

    def update_websocket_client_connection_details(self):
        self.websocket_client.set_websocket_url(
            self.settings.value("websocket_url", "")
        )
        self.websocket_client.set_websocket_port(
            self.settings.value("websocket_port", "")
        )
        self.websocket_client.set_websocket_password(
            self.settings.value("websocket_password", "")
        )
        self.websocket_client.retry_connection()

    def show_connection_setup(self):
        self.connection_setup_window = ConnectionSetupWindow(self.settings)
        self.connection_setup_window.accepted.connect(self.on_connection_setup_accepted)
        self.connection_setup_window.exec()

    @Slot()
    def on_connection_setup_accepted(self):
        websocket_connection_details = self.connection_setup_window.get_data()

        url = websocket_connection_details["url"]
        port = websocket_connection_details["port"]
        password = websocket_connection_details["password"]
        print(url, port, password)
        self.save_settings(url, port, password)
