import QtQuick

Window {
    objectName: "mainWindow"

    visible: true
    visibility: "FullScreen"
    flags: Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput
    color: "transparent"

    Overlay {
        isVisible: overlayController.isVisible
        overlayImageSource: overlayController.state == "recording"
            ? "qrc:/assets/images/record-icon.png"
            : "qrc:/assets/images/paused-icon.png"
    }
    
    ConfigureConnection {}
}