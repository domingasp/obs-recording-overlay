from typing import Protocol


class ISystemTrayIconView(Protocol):
    def create_tray_icon(self) -> None: ...
