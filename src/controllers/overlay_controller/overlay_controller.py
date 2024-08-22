from PySide6.QtCore import Property, QObject, Signal, Slot

from src.controllers.overlay_controller.overlay_controller_protocol import ObsState


class OverlayController(QObject):
    stateChanged = Signal()
    isVisibleChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state: ObsState = "recording"
        self._is_visible = False

    def get_state(self) -> bool:
        return self._state

    def get_is_visible(self) -> bool:
        return self._is_visible

    @Slot(str)
    def set_state(self, value: ObsState) -> None:
        self._state = value
        self.stateChanged.emit()

    @Slot(bool)
    def set_is_visible(self, value: bool) -> None:
        self._is_visible = value
        self.isVisibleChanged.emit()

    state = Property(str, get_state, set_state, notify=stateChanged)
    isVisible = Property(bool, get_is_visible, set_is_visible, notify=isVisibleChanged)
