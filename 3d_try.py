import pygame
from math import pi
from py3d import Camera, size, remake_s, remake_h, remake_v, dist, polygon_center, mc
from time import time

h = 50

if __name__ == '__main__':
    w = 0.05
    c = (0, 0, 0)
    p1 = (0, 0, 0)
    p2 = (h, 0, 0)
    p3 = (h, 0, h)
    p4 = (0, 0, h)
    p5 = (0, h, 0)
    p6 = (h, h, 0)
    p7 = (h, h, h)
    p8 = (0, h, h)
    clr1 = pygame.Color('red')
    clr2 = pygame.Color('green')
    clr3 = pygame.Color('blue')
    clr4 = pygame.Color('white')
    clr5 = pygame.Color('yellow')
    clr6 = pygame.Color('pink')
    pygame.init()
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    running = True
    camera = Camera((0, 0, -(3**0.5) * 150 - 600), (0, 0, -600))
    terrain = []
    p11 = (100, 100, 500)
    p22 = (100, 0, 500)
    p33 = (0, 0, 500)
    p44 = (0, 100, 500)
    for i in range(0, 20):
        for j in range(0, 20):
            c = (i * 50 - 500, -100, j * 50 - 500)
            c1 = (c[0] + 50, -100, c[2])
            c2 = (c[0] + 50, -100, c[2] + 50)
            c3 = (c[0], -100, c[2] + 50)
            terrain.append(([c, c1, c2, c3], dist(camera.pos, polygon_center([c, c1, c2, c3])), clr2))
    plane_map = []
    plane_map.extend(terrain)
    cube = [([p1, p5, p6, p2], dist(camera.pos, polygon_center([p1, p5, p6, p2])), clr1),
            ([p4, p8, p7, p3], dist(camera.pos, polygon_center([p4, p8, p7, p3])), clr2),
            ([p1, p5, p8, p4], dist(camera.pos, polygon_center([p1, p5, p8, p4])), clr3),
            ([p2, p6, p7, p3], dist(camera.pos, polygon_center([p2, p6, p7, p3])), clr4),
            ([p1, p2, p3, p4], dist(camera.pos, polygon_center([p1, p2, p3, p4])), clr5),
            ([p5, p6, p7, p8], dist(camera.pos, polygon_center([p5, p6, p7, p8])), clr6)]
    spaced = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    camera.move((0, 0, 100))
                if event.key == pygame.K_a:
                    camera.move((-100, 0, 0))
                if event.key == pygame.K_d:
                    camera.move((100, 0, 0))
                if event.key == pygame.K_x:
                    camera.move((0, 10, 0))
                if event.key == pygame.K_s:
                    camera.move((0, 0, -100))
                if event.key == pygame.K_z:
                    camera.turn_v(pi / 12)
                if event.key == pygame.K_c:
                    camera.turn_v(-pi / 12)
                if event.key == pygame.K_r:
                    camera.turn_h(pi / 12)
                if event.key == pygame.K_f:
                    camera.turn_h(-pi / 12)
                if event.key == pygame.K_SPACE:
                    spaced = 1
        hole_points = []
        hole_points.extend(cube)
        hole_points.extend(plane_map)
        hole_points.sort(key=lambda x: -x[1])
        for point in hole_points:
            square = mc(point[0], camera)
            if square != [(1, 1), (1, 1), (1, 1), (1, 1)]:
                pygame.draw.polygon(screen, point[2], square)
        pygame.draw.circle(screen, pygame.Color('red'), mc([(0, 0, 0)], camera)[0], 5)
        pygame.display.flip()
        screen.fill((0, 0, 0))
        p1 = remake_v(p1, w, (h / 2, p1[1], h / 2))
        p2 = remake_v(p2, w, (h / 2, p2[1], h / 2))
        p3 = remake_v(p3, w, (h / 2, p3[1], h / 2))
        p4 = remake_v(p4, w, (h / 2, p4[1], h / 2))
        p5 = remake_v(p5, w, (h / 2, p5[1], h / 2))
        p6 = remake_v(p6, w, (h / 2, p6[1], h / 2))
        p7 = remake_v(p7, w, (h / 2, p7[1], h / 2))
        p8 = remake_v(p8, w, (h / 2, p8[1], h / 2))
        p1 = remake_h(p1, w, (p1[0], h / 2, h / 2))
        p2 = remake_h(p2, w, (p2[0], h / 2, h / 2))
        p3 = remake_h(p3, w, (p3[0], h / 2, h / 2))
        p4 = remake_h(p4, w, (p4[0], h / 2, h / 2))
        p5 = remake_h(p5, w, (p5[0], h / 2, h / 2))
        p6 = remake_h(p6, w, (p6[0], h / 2, h / 2))
        p7 = remake_h(p7, w, (p7[0], h / 2, h / 2))
        p8 = remake_h(p8, w, (p8[0], h / 2, h / 2))
        cube = [([p1, p5, p6, p2], dist(camera.pos, polygon_center([p1, p5, p6, p2])), clr1),
                ([p4, p8, p7, p3], dist(camera.pos, polygon_center([p4, p8, p7, p3])), clr2),
                ([p1, p5, p8, p4], dist(camera.pos, polygon_center([p1, p5, p8, p4])), clr3),
                ([p2, p6, p7, p3], dist(camera.pos, polygon_center([p2, p6, p7, p3])), clr4),
                ([p1, p2, p3, p4], dist(camera.pos, polygon_center([p1, p2, p3, p4])), clr5),
                ([p5, p6, p7, p8], dist(camera.pos, polygon_center([p5, p6, p7, p8])), clr6)]
        pygame.time.Clock().tick(30)

