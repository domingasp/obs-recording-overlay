import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    visibility: Window.FullScreen
    title: "OBS Recording Overlay"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput
    color: "transparent"

    Rectangle {
        id: overlay
        width: 40
        height: 40
        color: "transparent"
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
        visible: true

        Image {
            id: statusImage
            anchors.fill: parent
            source: "../assets/record-icon.png"
        }
    }
}