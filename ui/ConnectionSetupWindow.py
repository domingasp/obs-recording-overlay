from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QToolButton,
    QHBoxLayout,
    QSizePolicy
)
from PySide6.QtGui import QIcon, QIntValidator
from PySide6.QtCore import Qt

from ui.ui_utilities import load_and_color_icon_pixmap


class ConnectionSetupWindow(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.load_icons()

        self.setWindowIcon(QIcon("assets/obs-recording-overlay-logo.png"))
        self.setWindowTitle("Configure OBS Connection")
        self.setFixedSize(300, 200)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.setup_url_fields()
        self.setup_obs_password_field()
        self.setup_save_button()

        self.set_initial_field_values()

    def setup_url_fields(self):
        """Initialize url and port fields."""
        label = QLabel("OBS Websocket Url:")
        self.main_layout.addWidget(label)

        url_port_layout = QHBoxLayout()

        self.url_field = QLineEdit()
        self.url_field.setPlaceholderText("URL")
        self.url_field.textChanged.connect(self.validate_fields)

        colon_separator = QLabel(":")

        self.port_field = QLineEdit()
        self.port_field.setMaximumWidth(60)
        self.port_field.setValidator(QIntValidator(0, 65535))
        self.port_field.setPlaceholderText("Port")
        self.port_field.textChanged.connect(self.validate_fields)

        url_port_layout.addWidget(self.url_field)
        url_port_layout.addWidget(colon_separator)
        url_port_layout.addWidget(self.port_field)
        self.main_layout.addLayout(url_port_layout)

        self.main_layout.addSpacing(8)

    def setup_obs_password_field(self):
        """Initialize password field with visibility control."""
        label = QLabel("OBS Websocket Password:")
        self.main_layout.addWidget(label)

        password_layout = QHBoxLayout()

        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.textChanged.connect(self.validate_fields)

        self.toggle_visibility_button = QToolButton()
        self.toggle_visibility_button.setIcon(self.icons["visible"])
        self.toggle_visibility_button.setCheckable(True)
        self.toggle_visibility_button.setToolTip("Show/Hide Password")
        self.toggle_visibility_button.setCursor(Qt.PointingHandCursor)
        self.toggle_visibility_button.setFixedHeight(34)
        self.toggle_visibility_button.clicked.connect(self.toggle_password_visibility)

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.toggle_visibility_button.setSizePolicy(size_policy)

        password_layout.addWidget(self.password_field)
        password_layout.addWidget(self.toggle_visibility_button)
        self.main_layout.addLayout(password_layout)

        self.main_layout.addSpacing(8)

    def setup_save_button(self):
        """Initialize save button."""
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        self.main_layout.addWidget(self.save_button)

    def set_initial_field_values(self):
        self.url_field.setText(self.settings.value("websocket_url", ""))
        self.port_field.setText(self.settings.value("websocket_port", ""))
        self.password_field.setText(self.settings.value("websocket_password", ""))

    def toggle_password_visibility(self):
        """Toggle `password_field` visibility."""
        if self.toggle_visibility_button.isChecked():
            self.password_field.setEchoMode(QLineEdit.Normal)
            self.toggle_visibility_button.setIcon(self.icons["notVisible"])
        else:
            self.password_field.setEchoMode(QLineEdit.Password)
            self.toggle_visibility_button.setIcon(self.icons["visible"])

    def validate_fields(self):
        """Validates the input fields for text and enables/disables `save_button`."""
        if (
            self.url_field.text()
            and self.port_field.text()
            and self.password_field.text()
        ):
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def get_data(self):
        return {
            "url": self.url_field.text(),
            "port": self.port_field.text(),
            "password": self.password_field.text(),
        }

    def load_icons(self):
        """Loads default icons."""
        self.icons = {
            "visible": load_and_color_icon_pixmap(
                icon_path="assets/icons/eye.svg", icon_color="white"
            ),
            "notVisible": load_and_color_icon_pixmap(
                icon_path="assets/icons/eye-off.svg", icon_color="white"
            ),
        }
