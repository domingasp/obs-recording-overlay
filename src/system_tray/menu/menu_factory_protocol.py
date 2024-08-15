from typing import Literal, Protocol, Union

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu


class IMenuFactory(Protocol):
    def create_menu(
        self, actions: list[Union[QAction, Literal["separator"]]], stylesheet_path: str
    ) -> QMenu: ...
