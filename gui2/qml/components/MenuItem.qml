import QtQuick 2.12
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.0

Button {
    id: menuItem

    property url btnImgSource: "../../images/files.svg"
    property color btnColorDefault: "#1b2529"
    property color btnColorMouseOver: "#293134"
    property color btnColorClicked: "#1b2529"
    property int btnImgSize: 30
    property string menuText: "Files"

    QtObject{
        id: internal
        property var dynamicColor: if(menuItem.down){
                                       menuItem.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       menuItem.hovered ? btnColorMouseOver : btnColorDefault
                                   }
        }

    width: 170
    height: 16
    visible: true
    anchors.leftMargin: 0

    implicitWidth: 170
    implicitHeight: 16

    background: Rectangle {
        color: internal.dynamicColor
        anchors.fill: parent
        Text {
                id: menuItemText
                anchors.left: menuItemImage.left
                anchors.leftMargin: 0
                anchors.right: parent.right
                anchors.rightMargin: 0
                anchors.verticalCenter: parent.verticalCenter
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.pixelSize: 16
                color: "#ffffff"
                text: menuText
            }
        Image {
            id: menuItemImage
            width: 16
            height: 16
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.verticalCenter: parent.verticalCenter
            fillMode: Image.PreserveAspectFit
            source: btnImgSource
        }
        ColorOverlay {
            anchors.fill: menuItemImage
            source: menuItemImage
            color: "#ffffff"
            antialiasing: false
        }
    }


}

