import QtQuick 2.12
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.0

Item {
    id: frame

    property int frameX: 170
    property int frameY: 150
    property int frameHeight: 170
    property int frameWidth: 150
    property color frameColor: "#ff0000"
    property string frameLabel: "person1"

    x: frameX
    y: frameY
    width: frameWidth
    height: frameHeight+20
    clip: false
    visible: true

    implicitWidth: frameHeight+20
    implicitHeight: frameWidth

    Label {
        id: frameTag
        text: qsTr(frameLabel)
        color: "#ffffff"
        height: 20
        width: frameWidth
        anchors.top: parent.top

    }

    Rectangle {
        id: frameBorder
        color: "#00000000"
        border.color: frameColor
        border.width: 3
        height: frameHeight
        width: frameWidth
        anchors.top: frameTag.bottom
    }
}

