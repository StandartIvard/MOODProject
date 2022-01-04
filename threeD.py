import pygame
from math import pi
from py3d import Camera, size, remake_s, remake_h, remake_v, dist, polygon_center, mc, Vector
from time import time
import sys
from funcForMap import translateMap


class Game:
    pause = False
    qtacess = False
    h = 50

    def __init__(self):
        pygame.init()
        self.game_init()

    def game_init(self):
        self.w = 0.05
        self.p1 = (0, 0, 0)
        self.p2 = (self.h, 0, 0)
        self.p3 = (self.h, 0, self.h)
        self.p4 = (0, 0, self.h)
        self.p5 = (0, self.h, 0)
        self.p6 = (self.h, self.h, 0)
        self.p7 = (self.h, self.h, self.h)
        self.p8 = (0, self.h, self.h)
        self.clr1 = pygame.Color('red')
        self.clr2 = pygame.Color('green')
        self.clr3 = pygame.Color('blue')
        self.clr4 = pygame.Color('white')
        self.clr5 = pygame.Color('yellow')
        self.clr6 = pygame.Color('pink')
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        self.running = True
        self.camera = Camera((0, 1750, -(3**0.5) * 200 - 600), (0, 1750, -600))
        self.terrain = []
        self.tecmap = 'mapName'
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
        cur_map = translateMap(self.tecmap, self.camera, self.clr3)
        self.plane_map = []
        self.plane_map.extend(cur_map)
        # self.plane_map.extend(self.terrain)
        # self.plane_map.append(([(-500, -500, 1000), (500, -500, 1000), (500, 500, 1000), (-500, 500, 1000)],
        #                     dist(self.camera.pos, polygon_center([(-500, -500, 1000), (500, -500, 1000), (500, 500, 1000), (-500, 500, 1000)])), self.clr1))
        # self.plane_map.extend(cur_map)
        self.cube = [([self.p1, self.p5, self.p6, self.p2], dist(self.camera.pos, polygon_center([self.p1, self.p5, self.p6, self.p2])), self.clr1),
                    ([self.p4, self.p8, self.p7, self.p3], dist(self.camera.pos, polygon_center([self.p4, self.p8, self.p7, self.p3])), self.clr2),
                    ([self.p1, self.p5, self.p8, self.p4], dist(self.camera.pos, polygon_center([self.p1, self.p5, self.p8, self.p4])), self.clr3),
                    ([self.p2, self.p6, self.p7, self.p3], dist(self.camera.pos, polygon_center([self.p2, self.p6, self.p7, self.p3])), self.clr4),
                    ([self.p1, self.p2, self.p3, self.p4], dist(self.camera.pos, polygon_center([self.p1, self.p2, self.p3, self.p4])), self.clr5),
                    ([self.p5, self.p6, self.p7, self.p8], dist(self.camera.pos, polygon_center([self.p5, self.p6, self.p7, self.p8])), self.clr6)]

        self.hole_points = []
        # self.hole_points.extend(self.cube)
        self.hole_points.extend(self.plane_map)
        self.stuck_polygons = []

    def main_loop(self, window):
        #print('ok')
        if self.qtacess:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                my_v = self.camera.move_vectors[0]
                self.camera.move(my_v.cords)
            if keys[pygame.K_a]:
                v = self.camera.move_vectors[1] * (-1)
                self.camera.move(v.cords)
            if keys[pygame.K_d]:
                v = self.camera.move_vectors[1]
                self.camera.move(v.cords)
            if keys[pygame.K_s]:
                v = self.camera.move_vectors[0] * (-1)
                self.camera.move(v.cords)
            if keys[pygame.K_LEFT]:
                self.camera.turn_v(pi / 20)
            if keys[pygame.K_RIGHT]:
                self.camera.turn_v(-pi / 20)
            if keys[pygame.K_ESCAPE]:
                self.qtacess = False
                self.pause = True
            self.hole_points.sort(key=lambda x: -x[1])
            self.stuck_polygons = []
            for point in self.hole_points:
                ind = self.hole_points.index(point)
                cur_color = self.hole_points[ind][2]
                cur_dist = dist(self.camera.pos, polygon_center(self.hole_points[ind][0]))
                cur_color.hsva = (cur_color.hsva[0], cur_color.hsva[1],
                                  max(0.01, min(1, 400 / cur_dist)) * 100,
                                  cur_color.hsva[3])
                self.hole_points[ind] = (self.hole_points[ind][0], cur_dist, cur_color)
                if cur_dist < 60:
                    self.stuck_polygons.append(Vector(self.hole_points[ind][0][0]) - Vector(self.hole_points[ind][0][1]))
                square = mc(point[0], self.camera)
                if square != [(1, 1), (1, 1), (1, 1), (1, 1)]:
                    pygame.draw.polygon(self.screen, point[2], square)
            pygame.draw.circle(self.screen, pygame.Color('red'), mc([(0, 0, 0)], self.camera)[0], 5)
            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            pygame.time.Clock().tick(30)
            return False
