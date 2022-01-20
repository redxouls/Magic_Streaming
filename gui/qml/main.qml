import QtQuick 2.12
import QtQuick.Window 2.0
import QtQuick.Controls 2.3
import "components"

Window {
    id: window
    width: 1080
    height: 640
    visible: true
    color: "#00000000"
    title: qsTr("Magic Streaming")

    flags: Qt.Window | Qt.FramelessWindowHint
    
    property int windowStatus: 0
    property int windowMargin: 10

    QtObject {
        id: internal
        function resizeWindow() {
            if (windowStatus==0) {
                window.showMaximized()
                max.btnImgSource =  "../images/restore.svg"
                windowStatus = 1
                windowMargin = 0
            } else if (windowStatus==1) {
                window.showNormal()
                max.btnImgSource = "../images/maximize.svg"
                windowStatus = 0
                windowMargin = 10
            }
        }
    }
    
    Rectangle {
        id: background
        color: "#374348"
        anchors.right: parent.right
        anchors.rightMargin: windowMargin
        anchors.left: parent.left
        anchors.leftMargin: windowMargin
        anchors.bottom: parent.bottom
        anchors.bottomMargin: windowMargin
        anchors.top: parent.top
        anchors.topMargin: windowMargin

        Rectangle {
            id: appContainer
            color: "#00000000"
            anchors.rightMargin: 1
            anchors.leftMargin: 1
            anchors.bottomMargin: 1
            anchors.topMargin: 1
            anchors.fill: parent

            Rectangle {
                id: navigator
                height: 30
                color: "#293134"
                anchors.right: parent.right
                anchors.rightMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: 0
                anchors.top: parent.top
                anchors.topMargin: 0

                DragHandler {
                    onActiveChanged: if(active) {
                        window.startSystemMove()
                    }
                }

                Toggle {
                    onClicked: menuAnimation.running = true
                }

                Label {
                    id: title
                    width: 120
                    text: qsTr("Magic Streaming")
                    color: "#ffffff"
                    anchors.left: parent.left
                    anchors.leftMargin: 35
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0
                    anchors.top: parent.top
                    anchors.topMargin: 0
                    verticalAlignment: Text.AlignVCenter
                }

                Row {
                    id: resize
                    x: 891
                    width: 120
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0
                    anchors.top: parent.top
                    anchors.topMargin: 0

                    Resize {
                        id: min
                        onClicked: window.showMinimized()
                    }
                    Resize {
                        id: max
                        btnImgSource: "../images/maximize.svg"
                        onClicked: internal.resizeWindow()
                    }
                    Resize {
                        id: close
                        btnImgSource: "../images/close.svg"
                        onClicked: window.close()
                    }
                }
            }

            Rectangle {
                id: control
                y: 528
                height: 90
                color: "#293134"
                anchors.right: parent.right
                anchors.rightMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: 0
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0

                Row {
                    id: controlBtn
                    x: 429
                    width: 370
                    height: 50
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 10
                    anchors.top: timelineContainer.bottom
                    anchors.topMargin: 0
                    spacing: 40

                    Control {
                        id: track
                        btnImgSource: "../images/track.svg"
                    }
                    Row {
                        id: speed
                        spacing: 20
                        Control {
                            id: backward
                            btnImgSource: "../images/backward.svg"
                        }
                        Control {
                            id: play
                        }
                        Control {
                            id: forward
                            btnImgSource: "../images/forward.svg"
                        }
                    }
                    Control {
                        id: replay
                        btnImgSource: "../images/replay.svg"
                        btnImgSize: 20
                    }
                }

                Rectangle {
                    id: timelineContainer
                    height: 30
                    color: "#00000000"
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    anchors.top: parent.top
                    anchors.topMargin: 0

                    Label {
                        id: startTime
                        x: 144
                        y: 8
                        text: qsTr("00:00")
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 4
                        anchors.right: progressBar.left
                        anchors.rightMargin: 40
                        color: "#ffffff"
                    }

                    ProgressBar {
                        id: progressBar
                        x: 212
                        y: 5
                        width: 700
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 10
                        anchors.horizontalCenter: parent.horizontalCenter
                        value: 0.5
                    }

                    Label {
                        id: endTime
                        y: 8
                        text: qsTr("00:00")
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 4
                        anchors.left: progressBar.right
                        anchors.leftMargin: 40
                        color: "#ffffff"
                    }
                }
            }

            Rectangle {
                id: content
                color: "#00000000"
                anchors.right: parent.right
                anchors.rightMargin: 0
                anchors.bottom: control.top
                anchors.bottomMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: 0
                anchors.top: navigator.bottom
                anchors.topMargin: 0

                Rectangle {
                    id: menu
                    width: 182
                    color: "#1b2529"
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    anchors.top: parent.top
                    anchors.topMargin: 0
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0

                    PropertyAnimation {
                        id: menuAnimation
                        target: menu
                        property: "width"
                        to: if (menu.width==30) return 185; else return 30
                        duration: 800
                        easing.type: Easing.InOutQuint
                    }


                    Rectangle {
                        id: menuContainer
                        color: "#00000000"
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 10
                        anchors.right: parent.right
                        anchors.rightMargin: 10
                        anchors.left: parent.left
                        anchors.leftMargin: 10
                        anchors.top: parent.top
                        anchors.topMargin: 10

                        LeftMenu {
                            anchors.right: parent.right
                            anchors.rightMargin: 0
                            anchors.left: parent.left
                            anchors.leftMargin: 0
                            anchors.top: parent.top
                            anchors.topMargin: 0

                        }

                    }
                }

                Rectangle {
                    id: viewPort
                    color: "#151b20"
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.left: menu.right
                    anchors.leftMargin: 0
                    anchors.top: parent.top
                    anchors.topMargin: 0
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 0

                    Frame {

                    }

                }
            }
        }
    }

}






