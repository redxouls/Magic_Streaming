# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtQml import QQmlApplicationEngine


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)


if __name__ == "__main__":
    app = QApplication([])
    engine = QQmlApplicationEngine()
    window = Main()
    engine.load('qml/main.qml')
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
#    window.show()
#    sys.exit(app.exec_())
