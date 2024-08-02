import logging
import sys
from PySide6.QtWidgets import QApplication

from logging_config import setup_logging
from ui.OverlayApp import OverlayApp

setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay_app = OverlayApp(app=app)
    sys.exit(app.exec())

    # if not engine.rootObjects():
    #     sys.exit(-1)

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
