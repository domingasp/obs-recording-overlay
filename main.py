import assets.assets_rc  # type: ignore
import src.stylesheets_rc  # type: ignore

import sys
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from src.system_tray.menu.menu_factory import MenuFactory
from src.system_tray.system_tray_view import SystemTrayIconView
from src.theme_controller import ThemeController


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.load("qml/themes/DefaultTheme.qml")
    engine.load("qml/Overlay.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    theme_controller = ThemeController(qml_engine=engine)
    menu_factory = MenuFactory(app, theme_controller)
    system_tray_icon = SystemTrayIconView(
        app,
        qml_engine=engine,
        theme_controller=theme_controller,
        menu_factory=menu_factory,
        icon_path=":/assets/images/logo.png",
    )
    system_tray_icon.create_tray_icon()

    sys.exit(app.exec())
