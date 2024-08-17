import QtQuick

Window {
    objectName: "mainWindow"

    visible: true
    visibility: "FullScreen"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput
    color: "transparent"

    Overlay {
        overlayImageSource: "qrc:/assets/images/record-icon.png"
    }
    
    ConfigureConnection {}
}