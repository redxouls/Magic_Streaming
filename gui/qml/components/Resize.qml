import QtQuick 2.12
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.0

Button {
    id: resize

    property url btnImgSource: "../../images/minimize.svg"
    property color btnColorDefault: "#293134"
    property color btnColorMouseOver: "#1b2529"
    property color btnColorClicked: "#293134"

    QtObject{
        id: internal
        property var dynamicColor: if(resize.down){
                                       resize.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       resize.hovered ? btnColorMouseOver : btnColorDefault
                                   }
        }

    width: 40
    height: 30
    clip: false
    visible: true

    implicitWidth: 30
    implicitHeight: 30

    background: Rectangle{
        id: resizeBtn
        color: internal.dynamicColor
        Image {
            id: resizeImage
            source: btnImgSource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: 16
            width: 16
            fillMode: Image.PreserveAspectFit
        }
        ColorOverlay {
            anchors.fill: resizeImage
            source: resizeImage
            color: "#ffffff"
            antialiasing: false
        }
    }
}

