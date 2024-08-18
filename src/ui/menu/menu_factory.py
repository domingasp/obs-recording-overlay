from typing import Literal, Union
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMenu, QWidgetAction

from .menu_factory_protocol import IMenuFactory
from src.controllers.theme_controller import IThemeController
from src.utils import load_stylesheet, replace_template_placeholders


class MenuFactory(IMenuFactory):
    def __init__(self, app: QApplication, theme_controller: IThemeController):
        self.app = app
        self.theme_controller = theme_controller

    def create_menu(
        self,
        actions: list[Union[QAction, QWidgetAction, Literal["separator"]]],
        stylesheet_path: str,
    ) -> QMenu:
        menu = QMenu()
        for action in actions:
            if action == "separator":
                menu.addSeparator()
            else:
                menu.addAction(action)

        self.__style_menu(stylesheet_path)
        return menu

    def __style_menu(self, stylesheet_path: str):
        app_stylesheet = self.app.styleSheet()
        menu_stylesheet = load_stylesheet(stylesheet_path)
        menu_stylesheet = replace_template_placeholders(
            menu_stylesheet,
            replacements=[
                {
                    "replace": r"%menuColor%",
                    "with_value": self.theme_controller.get_color("dark6"),
                },
                {
                    "replace": r"%borderColor%",
                    "with_value": self.theme_controller.get_color("dark4"),
                },
                {
                    "replace": r"%menuPadding%",
                    "with_value": str(
                        self.theme_controller.get_int_property("spacingXXS")
                    ),
                },
                {
                    "replace": r"%menuRadius%",
                    "with_value": str(
                        self.theme_controller.get_int_property("radiusSM")
                    ),
                },
                {
                    "replace": r"%menuItemColor%",
                    "with_value": self.theme_controller.get_color("colorText"),
                },
                {
                    "replace": r"%itemPaddingX%",
                    "with_value": str(
                        self.theme_controller.get_int_property("spacingSM")
                    ),
                },
                {
                    "replace": r"%itemPaddingY%",
                    "with_value": str(
                        self.theme_controller.get_int_property("spacingXXS")
                    ),
                },
                {
                    "replace": r"%itemFontSize%",
                    "with_value": str(
                        self.theme_controller.get_int_property("fontSizeXS")
                    ),
                },
                {
                    "replace": r"%iconSpacing%",
                    "with_value": str(
                        self.theme_controller.get_int_property("spacingXXS")
                    ),
                },
            ],
        )
        self.app.setStyleSheet(app_stylesheet + menu_stylesheet)
