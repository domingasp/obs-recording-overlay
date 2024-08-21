from typing import Protocol


class IListener(Protocol):
    def handle_event(self, event_type: str, data: dict) -> None: ...
