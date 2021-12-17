import pygame
from math import pi
from py3d import Camera, size, remake_s, remake_h, remake_v, dist, polygon_center, mc
from time import time
from MainMenuClass import MainMenu
from funcForWorkWithDB import getInformDB, insertUserDB
import sys
from PyQt5.QtWidgets import *
from uniAlertDialog import alertDialog

h = 50
chk = False


class Game:
    def __init__(self):
        pygame.init()
        self.game_init()

    def game_init(self):
        self.w = 0.05
        self.p1 = (0, 0, 0)
        self.p2 = (h, 0, 0)
        self.p3 = (h, 0, h)
        self.p4 = (0, 0, h)
        self.p5 = (0, h, 0)
        self.p6 = (h, h, 0)
        self.p7 = (h, h, h)
        self.p8 = (0, h, h)
        self.clr1 = pygame.Color('red')
        self.clr2 = pygame.Color('green')
        self.clr3 = pygame.Color('blue')
        self.clr4 = pygame.Color('white')
        self.clr5 = pygame.Color('yellow')
        self.clr6 = pygame.Color('pink')
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        self.running = True
        self.camera = Camera((0, 0, -(3**0.5) * 150 - 600), (0, 0, -600))
        self.terrain = []
        for i in range(0, 15):
            for j in range(0, 15):
                c = (i * 50 - 330, -100, j * 50 - 1000)
                c1 = (c[0] + 50, -100, c[2])
                c2 = (c[0] + 50, -100, c[2] + 50)
                c3 = (c[0], -100, c[2] + 50)
                self.terrain.append(([c, c1, c2, c3],
                        dist(self.camera.pos, polygon_center([c, c1, c2, c3])), self.clr2))
        for i in range(0, 15):
            for j in range(0, 15):
                c = (i * 50 - 330, 100, j * 50 - 1000)
                c1 = (c[0] + 50, 100, c[2])
                c2 = (c[0] + 50, 100, c[2] + 50)
                c3 = (c[0], 100, c[2] + 50)
                self.terrain.append(([c, c1, c2, c3],
                        dist(self.camera.pos, polygon_center([c, c1, c2, c3])), self.clr2))
        self.plane_map = []
        self.plane_map.extend(self.terrain)
        self.cube = [([self.p1, self.p5, self.p6, self.p2], dist(self.camera.pos, polygon_center([self.p1, self.p5, self.p6, self.p2])), self.clr1),
                    ([self.p4, self.p8, self.p7, self.p3], dist(self.camera.pos, polygon_center([self.p4, self.p8, self.p7, self.p3])), self.clr2),
                    ([self.p1, self.p5, self.p8, self.p4], dist(self.camera.pos, polygon_center([self.p1, self.p5, self.p8, self.p4])), self.clr3),
                    ([self.p2, self.p6, self.p7, self.p3], dist(self.camera.pos, polygon_center([self.p2, self.p6, self.p7, self.p3])), self.clr4),
                    ([self.p1, self.p2, self.p3, self.p4], dist(self.camera.pos, polygon_center([self.p1, self.p2, self.p3, self.p4])), self.clr5),
                    ([self.p5, self.p6, self.p7, self.p8], dist(self.camera.pos, polygon_center([self.p5, self.p6, self.p7, self.p8])), self.clr6)]

    def main_loop(self, window):
        global chk
        #print('ok')
        if chk:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                v = (0, 0, 25)
                v = remake_v(v, self.camera.ang_v, (0, 0, 0))
                v = remake_h(v, self.camera.ang_h, (0, 0, 0))
                v = remake_s(v, self.camera.ang_s, (0, 0, 0))
                self.camera.move(v)
            if keys[pygame.K_a]:
                v = (-25, 0, 0)
                v = remake_v(v, self.camera.ang_v, (0, 0, 0))
                v = remake_h(v, self.camera.ang_h, (0, 0, 0))
                v = remake_s(v, self.camera.ang_s, (0, 0, 0))
                self.camera.move(v)
            if keys[pygame.K_d]:
                v = (25, 0, 0)
                v = remake_v(v, self.camera.ang_v, (0, 0, 0))
                v = remake_h(v, self.camera.ang_h, (0, 0, 0))
                v = remake_s(v, self.camera.ang_s, (0, 0, 0))
                self.camera.move(v)
            if keys[pygame.K_s]:
                v = (0, 0, -25)
                v = remake_v(v, self.camera.ang_v, (0, 0, 0))
                v = remake_h(v, self.camera.ang_h, (0, 0, 0))
                v = remake_s(v, self.camera.ang_s, (0, 0, 0))
                self.camera.move(v)
            if keys[pygame.K_z]:
                self.camera.turn_v(pi / 20)
            if keys[pygame.K_c]:
                self.camera.turn_v(-pi / 20)
            self.hole_points = []
            self.hole_points.extend(self.cube)
            self.hole_points.extend(self.plane_map)
            self.hole_points.sort(key=lambda x: -x[1])
            for point in self.hole_points:
                ind = self.hole_points.index(point)
                self.hole_points[ind] = (self.hole_points[ind][0],
                        dist(self.camera.pos, polygon_center(self.hole_points[ind][0])),
                        self.hole_points[ind][2])
                square = mc(point[0], self.camera)
                if square != [(1, 1), (1, 1), (1, 1), (1, 1)]:
                    pygame.draw.polygon(self.screen, point[2], square)
            pygame.draw.circle(self.screen, pygame.Color('red'), mc([(0, 0, 0)], self.camera)[0], 5)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            self.p1 = remake_v(self.p1, self.w, (h / 2, self.p1[1], h / 2))
            self.p2 = remake_v(self.p2, self.w, (h / 2, self.p2[1], h / 2))
            self.p3 = remake_v(self.p3, self.w, (h / 2, self.p3[1], h / 2))
            self.p4 = remake_v(self.p4, self.w, (h / 2, self.p4[1], h / 2))
            self.p5 = remake_v(self.p5, self.w, (h / 2, self.p5[1], h / 2))
            self.p6 = remake_v(self.p6, self.w, (h / 2, self.p6[1], h / 2))
            self.p7 = remake_v(self.p7, self.w, (h / 2, self.p7[1], h / 2))
            self.p8 = remake_v(self.p8, self.w, (h / 2, self.p8[1], h / 2))
            self.p1 = remake_h(self.p1, self.w, (self.p1[0], h / 2, h / 2))
            self.p2 = remake_h(self.p2, self.w, (self.p2[0], h / 2, h / 2))
            self.p3 = remake_h(self.p3, self.w, (self.p3[0], h / 2, h / 2))
            self.p4 = remake_h(self.p4, self.w, (self.p4[0], h / 2, h / 2))
            self.p5 = remake_h(self.p5, self.w, (self.p5[0], h / 2, h / 2))
            self.p6 = remake_h(self.p6, self.w, (self.p6[0], h / 2, h / 2))
            self.p7 = remake_h(self.p7, self.w, (self.p7[0], h / 2, h / 2))
            self.p8 = remake_h(self.p8, self.w, (self.p8[0], h / 2, h / 2))
            self.cube = [([self.p1, self.p5, self.p6, self.p2], dist(self.camera.pos, polygon_center([self.p1, self.p5, self.p6, self.p2])), self.clr1),
                        ([self.p4, self.p8, self.p7, self.p3], dist(self.camera.pos, polygon_center([self.p4, self.p8, self.p7, self.p3])), self.clr2),
                        ([self.p1, self.p5, self.p8, self.p4], dist(self.camera.pos, polygon_center([self.p1, self.p5, self.p8, self.p4])), self.clr3),
                        ([self.p2, self.p6, self.p7, self.p3], dist(self.camera.pos, polygon_center([self.p2, self.p6, self.p7, self.p3])), self.clr4),
                        ([self.p1, self.p2, self.p3, self.p4], dist(self.camera.pos, polygon_center([self.p1, self.p2, self.p3, self.p4])), self.clr5),
                        ([self.p5, self.p6, self.p7, self.p8], dist(self.camera.pos, polygon_center([self.p5, self.p6, self.p7, self.p8])), self.clr6)]
            pygame.time.Clock().tick(30)
            return False


class Window(MainMenu, QWidget):
    def play(self):
        name = self.lineEdit.text()
        password = self.lineEdit_2.text()
        result = getInformDB(name)

        if len(result) == 0:
            alert = alertDialog("Пользователь с таким именем не найден")
            alert.show()

        elif result[0][1] != password:
            alert = alertDialog("Введён неверный пароль")
            alert.show()

        elif result[0][0] == name and result[0][1] == password:
            global chk
            chk = True


def main():
    game = Game()
    app = QApplication(sys.argv)
    ex = Window(game)
    result = app.exec_()
    print("Qt finished: " + str(result))
    sys.exit(result)


if __name__ == "__main__":
    main()

