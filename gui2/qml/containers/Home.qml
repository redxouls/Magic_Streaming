import QtQuick 2.12
import QtQuick.Window 2.10
import QtQuick.Controls 2.3

Item {

    property color btnColorDefault: "#7692bf"
    property color btnColorMouseOver: "#3b495f"
    property color btnColorClicked: "#3b495f"
    property int btnImgSize: 30

    QtObject{
        id: internal
        property var dynamicColor: if(button.down){
                                       button.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       button.hovered ? btnColorMouseOver : btnColorDefault
                                   }
        }
    width: 1080
    height: 640

    Rectangle {
        id: background
        color: "#232c2f"
        anchors.fill: parent

        Rectangle {
            id: rectangle
            x: 405
            y: 205
            width: 400
            height: 200
            color: "#00000000"
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter

            Label {
                id: label
                x: 169
                y: 18
                width: 209
                height: 68
                font.pixelSize: 50
                color: "#ffffff"
                text: qsTr("Welcome")
                anchors.bottom: button.top
                anchors.bottomMargin: 0
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Button {
                id: button
                x: 150
                y: 120
                width: 120
                height: 30
                anchors.horizontalCenter: parent.horizontalCenter
                background: Rectangle {
                    radius: 10
                    color: internal.dynamicColor
                }
                Label {
                    id: buttonText
                    text: qsTr("Setup")
                    color: button.onClicked ? "#0b0e13" : "#ffffff"
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }
    }

}

/*##^##
Designer {
    D{i:1;anchors_height:200;anchors_width:200;anchors_x:667;anchors_y:295}D{i:4;anchors_y:120}
}
##^##*/
