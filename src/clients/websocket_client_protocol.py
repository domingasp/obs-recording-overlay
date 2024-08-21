from typing import Protocol


class IWebSocketClient(Protocol):
    def run(self) -> None: ...
    def set_credentials(self, url: str, port: str, password: str) -> None: ...