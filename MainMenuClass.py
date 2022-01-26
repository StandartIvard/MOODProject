import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from funcForWorkWithDB import getInformDB, insertUserDB, updatePassword, updateHP
from uniAlertDialog import alertDialog
from passwordChangeDialog import passwordDialog


class MainMenu(QWidget):
    def __init__(self, game, parent=None):
        super().__init__(parent)
        loadUi(".//data/MainMenu.ui", self)

        self.name = ''

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

        self.init_pygame(game)

        self.secondForm = SecondMenu(self.game)
        self.deathScreen = deadScreen(self.game)

    def init_pygame(self, game):
        self.game = game
        self.timer = QTimer()
        self.timer.timeout.connect(self.pygame_loop)
        self.timer.start(0)

    def pygame_loop(self):
        self.deathScreen.name = self.name
        self.game.name = self.name
        if self.game.qtacess:
            result = getInformDB(self.name)

            self.game.HP = result[0][3]
            self.game.score = result[0][2]
        if self.game.main_loop(self):
            self.close()
        if self.game.pause and not self.game.dead:
            self.secondForm.name = self.name
            self.secondForm.show()
            self.secondForm.label.setText("Имя персонажа: " + self.secondForm.name)
            self.secondForm.label_2.setText("Очков: " + str(self.secondForm.score))
        if self.secondForm.cont or self.deathScreen.cont:
            self.game.pause = False

            self.secondForm.cont = False
            self.deathScreen.cont = False

            self.game.qtacess = True
            self.game.dead = False

            self.deathScreen.hide()
            self.secondForm.hide()
        if self.game.dead:
            self.deathScreen.show()
            self.game.pause = True

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
            self.lineEdit.setText("")
            self.lineEdit_2.setText("")
            self.game.qtacess = True
            self.game.pause = False
            self.hide()
            self.game.HP = result[0][3]
            self.name = result[0][0]
            self.game.score = result[0][2]

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


class SecondMenu(QWidget):

    def __init__(self, game, parent=None):
        super().__init__(parent)
        loadUi(".//data/PauseMenu.ui", self)
        oImage = QImage("data/images/screen2background.jpg")
        sImage = oImage.scaled(QSize(1429, 450))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.name = ""
        self.score = 0

        self.pushButton.clicked.connect(self.changePass)
        self.pushButton_2.clicked.connect(self.conti)

        self.cont = False

    def changePass(self):
        dlg = passwordDialog(self)
        dlg.exec_()
        tecpass, newpass, newpass2 = dlg.getPassword()

        result = getInformDB(self.name)

        self.score = result[0][2]

        if result[0][1] != tecpass:
            alert = alertDialog("Ваш старый пароль неверен")
            alert.exec_()
        elif newpass != newpass2:
            alert = alertDialog("Новые пароли не совпадают")
            alert.exec_()
        elif result[0][1] == tecpass and newpass == newpass2:
            updatePassword(self.name, newpass)
            alert = alertDialog("Ваш пароль успешно изменён")
            alert.exec_()

    def conti(self):
        self.cont = True


class deadScreen(QWidget):

    def __init__(self, game, parent=None):
        self.game = game
        super().__init__(parent)
        loadUi(".//data/deadScreen.ui", self)
        oImage = QImage("data/images/deathBackground.jpg")
        sImage = oImage.scaled(QSize(1429, 450))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.name = ""
        self.score = 0

        self.pushButton.clicked.connect(self.next)

        self.cont = False

    def next(self):
        self.cont = True
        self.game.HP = 100
        updateHP(self.name, 100)