import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import StyledControls 1.0
import DefaultStyle 1.0

Window {
    id: configureConnectionWindow
    objectName: "configureConnectionWindow"
    visible: false
    width: 325
    height: 240
    minimumWidth: 325
    minimumHeight: 240

    title: "Configure Connection"
    color: DefaultStyle.dark7

    Item {
        anchors.fill: parent
        anchors.margins: DefaultStyle.spacingSM

        ColumnLayout {
            anchors.fill: parent
            spacing: DefaultStyle.spacingSM


            Text {
                Layout.fillWidth: true
                
                text: "You'll need to enable OBS Websocket first."
                font.pixelSize: DefaultStyle.fontSizeSM
                font.weight: 600
                color: DefaultStyle.colorText
                horizontalAlignment: Text.AlignHCenter
                leftPadding: DefaultStyle.spacingXS
                rightPadding: DefaultStyle.spacingXS
            }

            HorizontalDivider {
                Layout.fillWidth: true
                Layout.preferredHeight: 2
            }

            RowLayout {
                Layout.fillHeight: false
                Layout.fillWidth: true
                spacing: DefaultStyle.spacingSM

                ColumnLayout {
                    Layout.fillWidth: true

                    Label {
                        text: "Url"
                    }

                    TextField {
                        Layout.fillWidth: true
                        id: urlField
                        placeholderText: "Url"
                        text: settingsController.url
                    }
                }

                Text {
                    Layout.fillHeight: true
                    text: ":"
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignBottom
                    bottomPadding: DefaultStyle.spacingXS - 1
                    font.pixelSize: DefaultStyle.fontSizeMD
                    font.weight: 900
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    Layout.preferredWidth: 75

                    Label {
                        text: "Port"
                    }

                    TextField {
                        Layout.fillWidth: true
                        id: portField
                        placeholderText: "Port"
                        validator: IntValidator {bottom: 0; top: 65535;} 
                        text: settingsController.port
                    }
                }
            }

            ColumnLayout {
                Layout.fillWidth: true

                Label {
                    text: "OBS Websocket Password"
                }

                TextField {
                    Layout.fillWidth: true
                    id: passwordField
                    placeholderText: "Password"
                    echoMode: TextInput.Password
                    text: settingsController.password
                }
            }

            Button {
                Layout.fillWidth: true
                Layout.fillHeight: true
                text: "Save"
                enabled: urlField.text.length > 0 && portField.text.length > 0 && passwordField.text.length > 0
                onClicked: {
                    settingsController.save_settings(urlField.text, portField.text, passwordField.text)
                    configureConnectionWindow.visible = false
                }
            }
        }
    }
}