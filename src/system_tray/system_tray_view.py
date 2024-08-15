from typing import Literal, Union
from PySide6.QtGui import QAction, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication, QSystemTrayIcon

from src.system_tray.menu.menu_factory_protocol import IMenuFactory
from src.system_tray.system_tray_view_protocol import ISystemTrayIconView
from src.theme_controller_protocol import IThemeController
from src.utils import create_colored_icon


class SystemTrayIconView(ISystemTrayIconView):
    def __init__(
        self,
        app: QApplication,
        qml_engine: QQmlApplicationEngine,
        menu_factory: IMenuFactory,
        theme_controller: IThemeController,
        icon_path: str,
    ):
        self.app = app
        self.qml_engine = qml_engine
        self.menu_factory = menu_factory
        self.theme_controller = theme_controller
        self.icon = icon_path

    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(QIcon(self.icon))

        self.action_configure_connection = self.__create_action(
            "Configure Connection",
            ":/assets/icons/settings.svg",
            self.theme_controller.get_color("colorText"),
        )
        self.action_exit = self.__create_action(
            "Quit",
            ":/assets/icons/power.svg",
            self.theme_controller.get_color("colorText"),
        )

        actions: list[Union[QAction, Literal["separator"]]] = [
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

    def __create_action(
        self, label: str, icon_path: str, icon_color_hex: str
    ) -> QAction:
        icon = create_colored_icon(icon_path, icon_color_hex)
        return QAction(
            icon,
            label,
        )
