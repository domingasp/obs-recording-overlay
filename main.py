import qml.qml_rc  # type: ignore
import assets.assets_rc  # type: ignore
import src.stylesheets_rc  # type: ignore

import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterSingletonType
from PySide6.QtWidgets import QApplication

from src.ui import (
    ITrayAction,
    ConfigureConnectionAction,
    QuitAction,
    MenuFactory,
    SystemTrayIconView,
)
from src.controllers import (
    ThemeController,
    SettingsController,
    OverlayController,
    ConnectionStatusController,
)
from src.events import EventManager, OverlayListener, ConnectionStatusListener


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

    settings_controller = SettingsController(app)
    overlay_controller = OverlayController(app)
    connection_status_controller = ConnectionStatusController(app)

    # region Events Setup
    overlay_listener = OverlayListener(overlay=overlay_controller)
    connection_status_listener = ConnectionStatusListener(
        connection_status=connection_status_controller
    )

    event_manager = EventManager()
    event_manager.register("connection", [connection_status_listener, overlay_listener])
    event_manager.register("status", [overlay_listener])
    # endregion

    context = engine.rootContext()
    context.setContextProperty("settingsController", settings_controller)
    context.setContextProperty("overlayController", overlay_controller)
    context.setContextProperty(
        "connectionStatusController", connection_status_controller
    )
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
        connection_status_controller=connection_status_controller,
        menu_factory=menu_factory,
        tray_actions=tray_actions,
        icon_path=":/assets/images/logo.png",
    )
    system_tray_icon.create_tray_icon()
    sys.exit(app.exec())
