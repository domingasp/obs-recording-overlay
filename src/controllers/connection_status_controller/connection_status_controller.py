from PySide6.QtCore import Property, QObject, Signal, Slot


class ConnectionStatusController(QObject):
    isConnectedChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isConnected = False

    def get_is_connected(self) -> bool:
        return self._isConnected

    @Slot(bool)
    def set_is_connected(self, value: bool) -> None:
        self._isConnected = value
        self.isConnectedChanged.emit()

    isConnected = Property(
        bool, get_is_connected, set_is_connected, notify=isConnectedChanged
    )
