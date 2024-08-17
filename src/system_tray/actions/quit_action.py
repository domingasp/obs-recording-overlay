from PySide6.QtWidgets import QApplication
from src.system_tray.actions.tray_action_protocol import ITrayAction


class QuitAction(ITrayAction):
    def __init__(self, app: QApplication):
        self.app = app

    def handle(self) -> None:
        self.app.quit()
