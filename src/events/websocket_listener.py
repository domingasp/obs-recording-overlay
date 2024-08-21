from typing import Literal

from src.clients.websocket_client_protocol import IWebSocketClient


class WebSocketListener:
    def __init__(self, ws: IWebSocketClient) -> None:
        self._ws = ws

    def handle_event(self, event_type: Literal["credentials"], data: dict) -> None:
        if event_type == "credentials":
            self._ws.set_credentials(
                url=data["url"], port=data["port"], password=data["password"]
            )
