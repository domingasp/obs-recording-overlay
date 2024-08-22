from typing import Literal

from src.controllers.connection_status_controller.connection_status_controller_protocol import (
    IConnectionStatusController,
)


class ConnectionStatusListener:
    def __init__(self, connection_status: IConnectionStatusController) -> None:
        self._connection_status = connection_status

    def handle_event(self, event_type: Literal["connection"], data: dict) -> None:
        if event_type == "connection":
            self._connection_status.set_is_connected(data["isConnected"])
