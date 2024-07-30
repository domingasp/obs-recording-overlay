import logging
import sys
import threading
from PySide6.QtWidgets import QApplication

from Overlay import Overlay
from WebSocketClient import WebSocketClient
from logging_config import setup_logging

setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.showFullScreen()

    ws_client = WebSocketClient(overlay)
    threading.Thread(target=ws_client.run, daemon=True).start()

    sys.exit(app.exec())
