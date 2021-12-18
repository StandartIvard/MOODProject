import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from funcForWorkWithDB import getInformDB, insertUserDB
from uniAlertDialog import alertDialog


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
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        result = getInformDB(name)

        if len(result) == 0:
            alert = alertDialog("Пользователь с таким именем не найден")
            alert.exec_()

        elif result[0][1] != password:
            alert = alertDialog("Введён неверный пароль")
            alert.exec_()

        elif result[0][0] == name and result[0][1] == password:
            self.game.chk = True

    def register(self):
        name = self.lineEdit_3.text()
        password1 = self.lineEdit_4.text()
        password2 = self.lineEdit_5.text()
        res = getInformDB(name)

        if len(res) == 0 and password1 == password2:
            insertUserDB(name, password1)
            alert = alertDialog("Вы успешно зарегистрировались")
            alert.exec_()
            self.lineEdit_3.setText("")
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")

        elif len(res) != 0:
            alert = alertDialog("Пользователь с таким именем уже существует")
            alert.exec_()
            self.lineEdit_3.setText("")

        elif password1 != password2:
            alert = alertDialog("Введённые пароли не совпадают")
            alert.exec_()
            self.lineEdit_4.setText("")
            self.lineEdit_5.setText("")