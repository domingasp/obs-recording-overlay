from typing import TypedDict, Union
from PySide6.QtCore import QObject, QUrl
from PySide6.QtGui import QAction
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtWidgets import QWidgetAction


from .create_colored_icon import create_colored_icon


class ContextPropertyDict(TypedDict):
    name: str
    value: any


def create_action(
    label: str,
    icon_path: str,
    icon_color_hex: str,
    parent: Union[QObject, None] = None,
) -> QAction:
    icon = create_colored_icon(icon_path, icon_color_hex)
    return QAction(icon, label, parent=parent)


def create_qml_action(
    parent: QObject, qml_path: str, contextProperty: ContextPropertyDict = None
) -> QWidgetAction:
    qml_widget = QQuickWidget()

    if contextProperty:
        qml_widget.rootContext().setContextProperty(
            contextProperty["name"], contextProperty["value"]
        )
    qml_widget.engine().addImportPath(":/")
    qml_widget.setSource(QUrl(qml_path))
    qml_widget.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)

    qml_action = QWidgetAction(parent)
    qml_action.setDefaultWidget(qml_widget)

    return qml_action
