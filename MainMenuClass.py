import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class MainMenu(QWidget):
    def __init__(self, parent=None):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec_())