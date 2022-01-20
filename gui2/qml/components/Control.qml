import QtQuick 2.12
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.0

Button {
    id: control

    property url btnImgSource: "../../images/play.svg"
    property color btnColorDefault: "#ffffff"
    property color btnColorMouseOver: "#a8a8b3"
    property color btnColorClicked: "#ffffff"
    property int btnImgSize: 30

    QtObject{
        id: internal
        property var dynamicColor: if(control.down){
                                       control.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       control.hovered ? btnColorMouseOver : btnColorDefault
                                   }
        }

    width: 50
    height: 50
    clip: false
    visible: true

    implicitWidth: 50
    implicitHeight: 50

    background: Rectangle{
        id: controlBtn
        color: "#293134"
        Image {
            id: controlImage
            source: btnImgSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: btnImgSize
            width: btnImgSize
            fillMode: Image.PreserveAspectFit
        }
        ColorOverlay {
            anchors.fill: controlImage
            source: controlImage
            color: internal.dynamicColor
            antialiasing: false
        }
    }
}

