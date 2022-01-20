import QtQuick 2.12
import QtQuick.Controls 2.3

Button {
    id: menuButton
    text: "Files"
    onClicked: menu.open()

    Menu {
        id: menu
        y: menuButton.height

        MenuItem {
            text: "New..."
        }
        MenuItem {
            text: "Open..."
        }
        MenuItem {
            text: "Save"
        }
    }

    width: 50
    height: 50
    clip: false
    visible: true

    implicitWidth: 50
    implicitHeight: 50

    background: Rectangle{
        id: menuBg
        color: "#293134"
    }
}
