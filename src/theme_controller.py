from PySide6.QtCore import QUrl
from PySide6.QtGui import QColor
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent

from src.theme_controller_protocol import IThemeController


class ThemeController(IThemeController):
    def __init__(self, qml_engine: QQmlApplicationEngine):
        self.qml_engine = qml_engine

        defaultStyleComponent = QQmlComponent(
            self.qml_engine,
            QUrl("qrc:/DefaultStyle/DefaultStyle.qml"),
            parent=self.qml_engine,  # prevents Garbage Collection
        )
        self.theme_object = defaultStyleComponent.create()

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
