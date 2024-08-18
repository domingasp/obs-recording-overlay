from PySide6.QtCore import QObject
from PySide6.QtQml import QQmlApplicationEngine

from .tray_action_protocol import ITrayAction


class ConfigureConnectionAction(ITrayAction):
    def __init__(self, qml_engine: QQmlApplicationEngine):
        self.qml_engine = qml_engine

    def handle(self) -> None:
        root_objects = self.qml_engine.rootObjects()

        for object in root_objects:
            if window := object.findChild(QObject, "configureConnectionWindow"):
                window.setProperty("visible", True)
