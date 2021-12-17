from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class alertDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        loadUi("data/alertDialog.ui", self)

        self.label.setText(text)
        self.label.adjustSize()