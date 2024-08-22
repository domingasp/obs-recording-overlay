from typing import Protocol

from src.events import IListener


class IEventManager(Protocol):
    def register(self, event_type: str, listener: list[IListener]) -> None: ...
    def unregister(self, event_type: str, listener: IListener) -> None: ...
    def notify(self, event_type: str, data=None) -> None: ...
