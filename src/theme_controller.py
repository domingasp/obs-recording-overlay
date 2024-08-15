from PySide6.QtGui import QColor
from PySide6.QtQml import QQmlApplicationEngine

from src.theme_controller_protocol import IThemeController


class ThemeController(IThemeController):
    def __init__(self, qml_engine: QQmlApplicationEngine):
        self.qml_engine = qml_engine
        self.theme_object = None

        root_objects = self.qml_engine.rootObjects()
        for object in root_objects:
            if object.objectName() == "theme":
                self.theme_object = object

    def get_color(self, name: str, default_color="#FF0000") -> str:
        if not self.theme_object:
            return default_color

        color = default_color
        property = self.theme_object.property(name)
        if property is not None and isinstance(property, QColor):
            color = property.name()

        return color

    def get_int_property(self, name: str, default_value=0) -> int:
        if not self.theme_object:
            return default_value

        property = self.theme_object.property(name)
        return property if property is not None else default_value
