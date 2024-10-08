import QtQuick

Rectangle {
    id: overlay

    property bool isVisible: false
    property string overlayImageSource: "qrc:/assets/images/paused-icon.png"

    width: 40
    height: 40
    color: "transparent"
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.bottomMargin: 10
    anchors.leftMargin: 10
    visible: overlay.isVisible

    Image {
        source: overlay.overlayImageSource
        anchors.fill: parent
    }
}