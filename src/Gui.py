import sys
import os
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QApplication, QSizePolicy
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QSlider
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, QTimer, QSize, Qt
from PIL.ImageQt import ImageQt

from client.Client import Client

class Window(QMainWindow):
    image_signal = pyqtSignal()

    def __init__(self, args, detector):
        super(Window, self).__init__()
        self.view_port = QLabel()
        self.target = QPushButton()
        self.setup_btn = QPushButton()
        self.play_btn = QPushButton()
        self.pause_btn = QPushButton()
        self.forward_btn = QPushButton()
        self.backward_btn = QPushButton()
        self.teardown_btn = QPushButton()
        self.volume = QSlider()
        self.error_label = QLabel()
        # self.client = Client(args, detector)
        self.image_signal.connect(self.reload_image)
        self.reload_timer = QTimer()
        self.reload_timer.timeout.connect(self.image_signal.emit)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Magic Streaming")

        self.view_port.setAlignment(Qt.AlignCenter)

        self.setup_btn.setEnabled(True)
        self.setup_btn.setText('Setup')
        self.setup_btn.clicked.connect(self.handle_setup)
        # self.setup_btn.setStyleSheet("")

        self.play_btn.setEnabled(False)
        self.play_btn.setStyleSheet("border:none;")
        self.play_btn.setIcon(QIcon('./images/play.svg'))
        self.play_btn.setIconSize(QSize(30,30))
        self.play_btn.clicked.connect(self.handle_play)

        self.pause_btn.setEnabled(False)
        self.pause_btn.setStyleSheet("border:none;")
        self.pause_btn.setIcon(QIcon('./images/pause.svg'))
        self.pause_btn.setIconSize(QSize(30,30))
        self.pause_btn.clicked.connect(self.handle_pause)

        self.teardown_btn.setEnabled(False)
        self.teardown_btn.setText('Teardown')
        self.teardown_btn.clicked.connect(self.handle_teardown)

        self.error_label.setSizePolicy(
            QSizePolicy.Preferred,
            QSizePolicy.Maximum)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(50, 0, 50, 0)
        control_layout.addWidget(self.setup_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.teardown_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.view_port)
        layout.addLayout(control_layout)
        layout.addWidget(self.error_label)

        central_widget.setLayout(layout)

    def handle_setup(self):
        # self.client.setup()
        self.setup_btn.setEnabled(False)
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(True)
        self.teardown_btn.setEnabled(True)
        self.reload_timer.start(0)

    def handle_play(self):
        # self.client.play()
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)

    def handle_pause(self):
        # self.client.pause()
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def handle_teardown(self):
        # self.client.tear_down()
        self.setup_btn.setEnabled(True)
        self.play_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)
        self.teardown_btn.setEnabled(False)
        self.view_port.clear()
        # disconnect ???

    def reload_image(self):
        # self.client.play() return frame or pix ???

        # frame = self.client.play()
        # pix = QPixmap.fromImage(ImageQt(frame[0]).copy())
        # self.view_port.setPixmap(pix)
        self.view_port.setPixmap(QPixmap("./images/heart.svg"))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window(1, 1)

    available_geometry = window.screen().availableGeometry()
    window.resize(available_geometry.width() / 3,
                    available_geometry.height() / 2)
    window.show()
    sys.exit(app.exec())
