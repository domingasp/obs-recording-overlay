import assets.assets_rc  # type: ignore

import sys
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.load("qml/Overlay.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
