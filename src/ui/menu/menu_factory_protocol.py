from typing import Literal, Protocol, Union

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QWidgetAction


class IMenuFactory(Protocol):
    def create_menu(
        self,
        actions: list[Union[QAction, QWidgetAction, Literal["separator"]]],
        stylesheet_path: str,
    ) -> QMenu: ...
