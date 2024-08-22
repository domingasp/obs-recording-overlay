import qml.qml_rc  # type: ignore
import assets.assets_rc  # type: ignore
import src.stylesheets_rc  # type: ignore

import logging
from logging_config import setup_logging

import sys
import threading
import os

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
from src.events import (
    EventManager,
    OverlayListener,
    ConnectionStatusListener,
    WebSocketListener,
)
from src.clients import WebSocketClient
from src.utils import SingleInstance


setup_logging()
logger = logging.getLogger(__name__)


def create_tray_actions(
    engine: QQmlApplicationEngine, app: QApplication
) -> dict[str, ITrayAction]:
    return {
        "configure_connection": ConfigureConnectionAction(qml_engine=engine),
        "quit": QuitAction(app=app),
    }


if __name__ == "__main__":
    lockfile = os.path.join(
        os.getenv("LOCALAPPDATA"), "OBS Recording Overlay", "obs-recording-app.lock"
    )
    instance = SingleInstance(lockfile)

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine(app)

    event_manager = EventManager()
    settings_controller = SettingsController(event_manager=event_manager, parent=app)
    overlay_controller = OverlayController(app)
    connection_status_controller = ConnectionStatusController(app)
    ws_client = WebSocketClient(
        event_manager=event_manager,
        url=settings_controller.get_url(),
        port=settings_controller.get_port(),
        password=settings_controller.get_password(),
    )

    # region Events Setup
    overlay_listener = OverlayListener(overlay=overlay_controller)
    connection_status_listener = ConnectionStatusListener(
        connection_status=connection_status_controller
    )
    websocket_listener = WebSocketListener(ws=ws_client)

    event_manager.register("connection", [connection_status_listener, overlay_listener])
    event_manager.register("status", [overlay_listener])
    event_manager.register("credentials", [websocket_listener])
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

    threading.Thread(target=ws_client.run, daemon=True).start()

    sys.exit(app.exec())
