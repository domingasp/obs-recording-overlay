import QtQuick
import QtQuick.Controls.Basic

import DefaultStyle 1.0

Button {
    id: control
    text: qsTr("Button")

    contentItem: Text {
        text: control.text
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
        color: control.enabled ? "white" : DefaultStyle.dark3
        font.weight: 700
        font.pixelSize: DefaultStyle.fontSizeSM
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 30
        radius: DefaultStyle.radiusSM
        color: !control.enabled ? DefaultStyle.dark6
            : control.hovered
                ? DefaultStyle.blue9 : DefaultStyle.blue8
    
        Behavior on color {
            ColorAnimation {
                duration: 100
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        onPressed: mouse.accepted = false
        cursorShape: control.enabled ? Qt.PointingHandCursor : Qt.ForbiddenCursor
    }
}