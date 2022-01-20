import QtQuick 2.12
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.0

Button {
    id: toggle

    property url btnImgSource: "../../images/menu.svg"
    property color btnColorDefault: "#293134"
    property color btnColorMouseOver: "#1b2529"
    property color btnColorClicked: "#293134"

    QtObject{
        id: internal
        property var dynamicColor: if(toggle.down){
                                       toggle.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       toggle.hovered ? btnColorMouseOver : btnColorDefault
                                   }
        }

    width: 30
    height: 30
    clip: false
    visible: true

    implicitWidth: 30
    implicitHeight: 30

    background: Rectangle{
        id: toggleBtn
        color: internal.dynamicColor
        Image {
            id: toggleImage
            source: btnImgSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 20
            width: 20
            fillMode: Image.PreserveAspectFit
        }
        ColorOverlay {
            anchors.fill: toggleImage
            source: toggleImage
            color: "#ffffff"
            antialiasing: false
        }
    }
}

