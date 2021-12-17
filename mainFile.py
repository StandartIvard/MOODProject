from funcForWorkWithDB import getInformDB, insertUserDB

from MainMenuClass import MainMenu
from threeD import Game

from PyQt5.QtWidgets import *

import sys


def main():
    game = Game()
    app = QApplication(sys.argv)
    ex = MainMenu(game)
    result = app.exec_()
    print("Qt finished: " + str(result))
    sys.exit(result)


if __name__ == "__main__":
    main()