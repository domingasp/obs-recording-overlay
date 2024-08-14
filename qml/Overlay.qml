import QtQuick 2.15
import QtQuick.Controls 2.15

Window {
    visible: true
    visibility: "FullScreen"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput
    color: "transparent"

    Rectangle {
        id: overlay
        property string overlayImageSource: "qrc:/assets/images/paused-icon.png"

        width: 40
        height: 40
        color: "transparent"
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
        visible: true

        Image {
            source: overlay.overlayImageSource
            anchors.fill: parent
        }
    }
}