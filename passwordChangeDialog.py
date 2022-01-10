from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class passwordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("data/changeDialog.ui", self)
        
        self.pushButton.clicked.connect(self.echomod)

        self.chk = False

        self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
        self.lineEdit_3.setEchoMode(QLineEdit.EchoMode.Password)
    
    def echomod(self):
        if self.chk:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Normal)
            self.chk = False
        else:
            self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)
            self.lineEdit_2.setEchoMode(QLineEdit.EchoMode.Password)
            self.chk = True

    def getPassword(self):
        return self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()