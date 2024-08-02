import logging
import sys
import threading
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from WebSocketClient import WebSocketClient
from logging_config import setup_logging
from ui.__Overlay import Overlay

setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = QGuiApplication()
    engine = QQmlApplicationEngine()

    engine.load(QUrl('ui/main.qml'))

    # if not engine.rootObjects():
    #     sys.exit(-1)

    sys.exit(app.exec())
    # app = QApplication(sys.argv)
    # app.setQuitOnLastWindowClosed(False)

    # with open("ui/styles/styles.qss", "r") as file:
    #     stylesheet = file.read()
    # app.setStyleSheet(stylesheet)

    # overlay = Overlay()
    # overlay.showFullScreen()

    # ws_client = WebSocketClient(overlay)
    # threading.Thread(target=ws_client.run, daemon=True).start()

    # overlay.set_websocket_client(websocket_client=ws_client)

    # sys.exit(app.exec())
