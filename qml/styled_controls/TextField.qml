import QtQuick
import QtQuick.Controls.Basic

import DefaultStyle 1.0

TextField {
    id: control
    placeholderText: qsTr("Enter description")

    color: DefaultStyle.colorText
    placeholderTextColor: DefaultStyle.dark3

    background: Rectangle {
        implicitWidth: 200
        implicitHeight: 32
        color: DefaultStyle.dark6
        border.color: control.focus ? DefaultStyle.blue8 : DefaultStyle.dark4
        radius: DefaultStyle.radiusSM

        Behavior on border.color {
            ColorAnimation {
                duration: 100
            }
        }
    }
}