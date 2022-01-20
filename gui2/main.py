# This Python file uses the following encoding: utf-8
import sys
import os
import datetime

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtCore import QObject, Slot, Signal, QTimer, QUrl


class Main(QObject):
    def __init__(self):
        QObject.__init__(self)

    setup = Signal(bool)
    teardown = Signal(bool)
    labelbox = Signal(bool)
    playpause = Signal(bool)
    path = Signal(str)

    @Slot(bool)
    def toggleSetup(self, isClicked):
        self.setup.emit(isClicked)
        print("setup successfully")
        print(isClicked)

    @Slot(bool)
    def toggleTeardown(self, isClicked):
        self.teardown.emit(isClicked)
        print("teardown")

    @Slot(bool)
    def getLabel(self, isClicked):
        self.labelbox.emit(isClicked)
        print("obtain label box information")

    @Slot(bool)
    def getPlayPause(self, isPlaying):
        self.playpause.emit()
        print(isPlaying)

    # @Slot(str)
    def showImage(self, imgPath):
        self.path.emit(imgPath)
        print("show ", imgPath)


if __name__ == "__main__":
    app = QGuiApplication([])
    engine = QQmlApplicationEngine()
    window = Main()
    window.showImage("./images/two.jpg")
    engine.rootContext().setContextProperty("backend", window)
    engine.load('qml/main.qml')
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())
#    window.show()
#    sys.exit(app.exec_())
