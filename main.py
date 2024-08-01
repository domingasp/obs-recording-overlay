import logging
import sys
import threading
from PySide6.QtWidgets import QApplication

from WebSocketClient import WebSocketClient
from logging_config import setup_logging
from ui.Overlay import Overlay

setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    with open("ui/styles/styles.qss", "r") as file:
        stylesheet = file.read()
    app.setStyleSheet(stylesheet)

    overlay = Overlay()
    overlay.showFullScreen()

    ws_client = WebSocketClient(overlay)
    threading.Thread(target=ws_client.run, daemon=True).start()

    sys.exit(app.exec())
