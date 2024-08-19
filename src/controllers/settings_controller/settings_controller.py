from PySide6.QtCore import Property, QObject, QSettings, Signal, Slot
import keyring


class SettingsController(QObject):
    urlChanged = Signal()
    portChanged = Signal()
    passwordChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._settings = QSettings("DomingasP", "OBSRecordingOverlay")
        self._service_name = "OBSRecordingOverlay"

    def get_url(self) -> str:
        return self._settings.value("url", "")

    def set_url(self, value: str) -> None:
        if value != self.get_url():
            self._settings.setValue("url", value)
            self.urlChanged.emit()

    url = Property(str, get_url, set_url, notify=urlChanged)

    def get_port(self) -> str:
        return self._settings.value("port", "")

    def set_port(self, value: str) -> None:
        if value != self.get_url():
            self._settings.setValue("port", value)
            self.portChanged.emit()

    port = Property(str, get_port, set_port, notify=portChanged)

    def get_password(self) -> str:
        password = keyring.get_password(self._service_name, "password")
        return password if password else ""

    def set_password(self, value: str) -> None:
        if value != self.get_password():
            keyring.set_password(self._service_name, "password", value)
            self.passwordChanged.emit()

    password = Property(str, get_password, set_password, notify=passwordChanged)

    @Slot(str, str, str)
    def save_settings(self, url: str, port: str, password: str) -> None:
        self.set_url(url)
        self.set_port(port)
        self.set_password(password)
