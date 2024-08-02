from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon


class OverlayApp:
    def __init__(self, app: QApplication):
        self.app = app
        self.engine = QQmlApplicationEngine()

        self.load_stylesheets(["ui/styles/system-tray-icon.styles.qss"])

        self.setup_system_tray_icon()

    def load_stylesheets(self, files: list[str]):
        """Loads `files` and applies them at the application level."""
        qss = ""
        for path in files:
            with open(path, "r") as file:
                qss += file.read() + "\n"

        self.app.setStyleSheet(qss)

    def setup_system_tray_icon(self):
        """Initialises the system tray icon with the context menu."""
        system_tray_icon = QSystemTrayIcon(
            QIcon("assets/obs-recording-overlay-logo.png"), self.app
        )
        system_tray_icon.setToolTip("OBS Recording Overlay")

        tray_menu = QMenu()
        tray_menu.setFixedWidth(150)
        configure_connection = tray_menu.addAction("Configure Connection")
        tray_menu.addSeparator()
        exit_action = tray_menu.addAction("Exit")

        exit_action.triggered.connect(self.app.quit)

        system_tray_icon.setContextMenu(tray_menu)
        system_tray_icon.show()
