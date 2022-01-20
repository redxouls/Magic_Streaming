import QtQuick 2.12
import QtQuick.Controls 2.3
import QtGraphicalEffects 1.0

Button {
    id: play

    property url btnImgPlay: "../../images/play.svg"
    property url btnImgPause: "../../images/pause.svg"
    property color btnColorDefault: "#ffffff"
    property color btnColorMouseOver: "#a8a8b3"
    property color btnColorClicked: "#ffffff"
    property int btnImgSize: 30
    property bool isPlaying: false

    QtObject{
        id: internal
        property var dynamicColor: if(play.down){
                                       play.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       play.hovered ? btnColorMouseOver : btnColorDefault
                                   }
        
        // property var dynamicImage: if(isPlaying){
        //                                isPlaying ? btnImgPlay : btnImgPause
        //                            }
        }

    width: 50
    height: 50
    clip: false
    visible: true

    implicitWidth: 50
    implicitHeight: 50

    background: Rectangle{
        id: playBtn
        color: "#293134"
        Image {
            id: playImage
            source: "../../images/play.svg"
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            height: btnImgSize
            width: btnImgSize
            fillMode: Image.PreserveAspectFit
            function reload() {
                source = isPlaying ? btnImgPause : btnImgPlay
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    parent.reload()
                    isPlaying = !isPlaying
                    console.log(play.isPlaying)
                    // backend.getPlayPause(isPlaying=isPlaying.toString())
                }
            }
            // Connections{
            //     target: backend
            //     function onPlaypause(isPlaying){
            //         console.info("here")
            //     }
            // }
        }
        ColorOverlay {
            anchors.fill: playImage
            source: playImage
            color: internal.dynamicColor
            antialiasing: false
        }
    }
}

