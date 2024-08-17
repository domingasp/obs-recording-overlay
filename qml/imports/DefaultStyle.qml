pragma Singleton
import QtQuick

QtObject {
    id: theme
    objectName: "theme"

    // Values from mantine.dev
    readonly property color dark0: "#c9c9c9"
    readonly property color dark3: "#696969"
    readonly property color dark4: "#424242"
    readonly property color dark5: "#3b3b3b"
    readonly property color dark6: "#2e2e2e"
    readonly property color dark7: "#242424"

    readonly property color red6: "#fa5252"

    readonly property color green6: "#40c057"

    readonly property color blue8: "#1971c2"
    readonly property color blue9: "#1864ab"

    readonly property alias colorText: theme.dark0

    readonly property int radiusXS: 2
    readonly property int radiusSM: 4
    readonly property int radiusMD: 8
    readonly property int radiusLG: 16
    readonly property int radiusXL: 32

    readonly property int fontSizeXS: 12
    readonly property int fontSizeSM: 14
    readonly property int fontSizeMD: 16
    readonly property int fontSizeLG: 18
    readonly property int fontSizeXL: 20

    readonly property int spacingXXS: 4
    readonly property int spacingXS: 10
    readonly property int spacingSM: 12
    readonly property int spacingMD: 16
    readonly property int spacingLG: 20
    readonly property int spacingXL: 32
}
