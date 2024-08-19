from typing import Literal, Union
from PySide6.QtGui import QAction, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QWidgetAction

from src.controllers.theme_controller import IThemeController
from src.ui.menu import IMenuFactory
from src.ui.actions import ITrayAction
from src.utils import create_action, create_qml_action


class SystemTrayIconView:
    def __init__(
        self,
        app: QApplication,
        qml_engine: QQmlApplicationEngine,
        menu_factory: IMenuFactory,
        theme_controller: IThemeController,
        tray_actions: dict[str, ITrayAction],
        icon_path: str,
    ):
        self.app = app
        self.qml_engine = qml_engine
        self.menu_factory = menu_factory
        self.theme_controller = theme_controller
        self.tray_actions = tray_actions
        self.icon = icon_path

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(self.app)
        self.tray_icon.setIcon(QIcon(self.icon))

        self.action_connection_status = create_qml_action(
            self.tray_icon, "qrc:/qml/ConnectionStatus.qml"
        )
        self.action_configure_connection = create_action(
            "Configure Connection",
            ":/assets/icons/settings.svg",
            self.theme_controller.get_color("colorText"),
            parent=self.tray_icon,
        )
        self.action_exit = create_action(
            "Quit",
            ":/assets/icons/power.svg",
            self.theme_controller.get_color("colorText"),
            parent=self.tray_icon,
        )

        self.action_configure_connection.triggered.connect(
            self.tray_actions["configure_connection"].handle
        )
        self.action_exit.triggered.connect(self.tray_actions["quit"].handle)

        actions: list[Union[QAction, QWidgetAction, Literal["separator"]]] = [
            self.action_connection_status,
            "separator",
            self.action_configure_connection,
            "separator",
            self.action_exit,
        ]
        self.tray_icon.setContextMenu(
            self.menu_factory.create_menu(
                actions, ":/stylesheets/system_tray.styles.qss"
            )
        )
        self.tray_icon.show()
