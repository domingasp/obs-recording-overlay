from typing import Literal
from src.controllers import OverlayController


class OverlayListener:
    def __init__(self, overlay: OverlayController) -> None:
        self._overlay = overlay

    def handle_event(
        self, event_type: Literal["status", "connection"], data: dict
    ) -> None:
        if event_type == "status":
            self._overlay.set_state(data["status"])
        elif event_type == "connection":
            self._overlay.set_is_visible(data["isConnected"])
