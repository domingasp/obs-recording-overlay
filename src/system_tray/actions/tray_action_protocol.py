from typing import Protocol


class ITrayAction(Protocol):
    def handle(self) -> None: ...
