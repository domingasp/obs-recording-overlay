from src.events import IListener


class EventManager:
    def __init__(self):
        self._listeners: dict[str, list[IListener]] = {}

    def register(self, event_type: str, listeners: list[IListener]) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []

        self._listeners[event_type].extend(listeners)

    def unregister(self, event_type: str, listener: IListener) -> None:
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def notify(self, event_type: str, data=None) -> None:
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener.handle_event(event_type, data)
