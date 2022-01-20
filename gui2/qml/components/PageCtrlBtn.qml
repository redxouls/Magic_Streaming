import QtQuick 2.12
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.0

Button {
    id: pageBtn
    property string btnText: "teardown"
    property color textColorDefault: "#ffffff"
    property color textColorHovered: "#a8a8b3"
    property color textColorClicked: "#ffffff"
    property bool isActive: false

    QtObject{
        id: internal
        property var textDynamicColor: if(pageBtn.down){
                                       pageBtn.down ? textColorClicked : textColorDefault
                                   } else {
                                       pageBtn.hovered ? textColorHovered : textColorDefault
                                   }
        }

    width: 120
    height: 30
    anchors.verticalCenter: parent.verticalCenter
    background: Rectangle {
        radius: 10
        color: "#1b2529"
    }
    Label {
        id: buttonText
        text: qsTr(btnText)
        color: internal.textDynamicColor
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
    }
}


