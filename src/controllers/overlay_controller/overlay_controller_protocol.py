from typing import Literal, Protocol

from PySide6.QtCore import Slot

ObsState = Literal["recording", "paused"]


class IOverlayController(Protocol):
    def get_state(self) -> bool: ...
    def get_is_visible(self) -> bool: ...

    @Slot(str)
    def set_state(self, value: ObsState) -> None: ...

    @Slot(bool)
    def set_is_visible(self, value: bool) -> None: ...
