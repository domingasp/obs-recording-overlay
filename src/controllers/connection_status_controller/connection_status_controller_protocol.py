from typing import Protocol

from PySide6.QtCore import Slot


class IConnectionStatusController(Protocol):
    def get_is_connected(self) -> bool: ...

    @Slot(bool)
    def set_is_connected(self, value: bool) -> None: ...
