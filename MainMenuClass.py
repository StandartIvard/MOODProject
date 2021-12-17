import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MainMenu(QWidget):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        loadUi(".//data/MainMenu.ui", self)

        self.pixmap = QPixmap('data/images/logo.png')
        self.label.setPixmap(self.pixmap)

        oImage = QImage("data/images/Background.png")
        sImage = oImage.scaled(QSize(1429, 450))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)
        self.show()

        self.pushButton_2.clicked.connect(self.play)
        self.pushButton_3.clicked.connect(self.register)

        self.label_2.adjustSize()
        self.label_3.adjustSize()

        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_4.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_5.setEchoMode(QLineEdit.EchoMode.Password)

        self.lineEdit_2.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')

        self.init_pygame(game)

    def init_pygame(self, game):
        self.game = game
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(0)

    def pygame_loop(self):
        if self.game.main_loop(self):
            self.close()

    def play(self):
        pass

    def register(self):
        pass