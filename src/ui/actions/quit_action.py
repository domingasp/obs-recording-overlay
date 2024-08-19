from PySide6.QtWidgets import QApplication


class QuitAction:
    def __init__(self, app: QApplication):
        self.app = app

    def handle(self) -> None:
        self.app.quit()
