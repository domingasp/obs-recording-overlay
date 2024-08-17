import qml.qml_rc  # type: ignore
import assets.assets_rc  # type: ignore
import src.stylesheets_rc  # type: ignore

import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType
from PySide6.QtWidgets import QApplication

from src.system_tray.menu.menu_factory import MenuFactory
from src.system_tray.system_tray_view import SystemTrayIconView
from src.theme_controller import ThemeController
from src.system_tray.actions.quit_action import QuitAction
from src.system_tray.actions.configure_connection_action import (
    ConfigureConnectionAction,
)
from src.system_tray.actions.tray_action_protocol import ITrayAction


def create_tray_actions(
    engine: QQmlApplicationEngine, app: QApplication
) -> dict[str, ITrayAction]:
    return {
        "configure_connection": ConfigureConnectionAction(qml_engine=engine),
        "quit": QuitAction(app=app),
    }


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine(app)
    engine.addImportPath(":/")

    engine.load(":/qml/main.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    qmlRegisterSingletonType(
        QUrl("qrc:/DefaultStyle/DefaultStyle.qml"), "DefaultStyle", 1, 0, "DefaultStyle"
    )
    app.setWindowIcon(QIcon(":/assets/images/logo.png"))

    theme_controller = ThemeController(qml_engine=engine)
    menu_factory = MenuFactory(app, theme_controller)
    tray_actions = create_tray_actions(engine, app)

    system_tray_icon = SystemTrayIconView(
        app,
        qml_engine=engine,
        theme_controller=theme_controller,
        menu_factory=menu_factory,
        tray_actions=tray_actions,
        icon_path=":/assets/images/logo.png",
    )
    system_tray_icon.create_tray_icon()
    sys.exit(app.exec())
