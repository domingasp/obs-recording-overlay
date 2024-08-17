import QtQuick
import QtQuick.Effects

import DefaultStyle 1.0

Rectangle {
    id: connectionStatus

    property bool isConnected: false
    property color componentColor: connectionStatus.isConnected ? DefaultStyle.green6 : DefaultStyle.red6

    width: 100
    height: 32
    color: DefaultStyle.dark6

    Row {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        spacing: DefaultStyle.spacingXS

        Item {
            width: 24
            height: 24
            anchors.verticalCenter: parent.verticalCenter

            Image {
                id: statusIcon
                source: "qrc:/assets/icons/circle.svg"
                anchors.centerIn: parent
                visible: false
            }

            MultiEffect {
                colorizationColor: connectionStatus.componentColor
                
                source: statusIcon
                anchors.fill: statusIcon
                colorization: 1.0
            }
        }

        Text {
            text: connectionStatus.isConnected ? qsTr("Connected") : qsTr("Disconnected")
            
            color: connectionStatus.componentColor
            anchors.verticalCenter: parent.verticalCenter
            font.pixelSize: DefaultStyle.fontSizeSM
            font.weight: 600
        }
    }
}
