import pygame
from math import sin, cos, pi

size = [600, 600]
CENTER = (size[0] / 2, size[1] / 2, 0)
h = 50


class Camera:
    def __init__(self, pos=(0, 0, 0), field=(0, 0, 1), ang_vert=0, ang_hor=0, ang_st=0):
        self.field = field
        self.pos = pos
        self.ang_v = ang_vert
        self.ang_h = ang_hor
        self.ang_s = ang_st

    def turn_h(self, rad):
        self.field = remake_h(self.field, rad, self.pos)
        self.ang_h += rad

    def turn_v(self, rad):
        self.field = remake_v(self.field, rad, self.pos)
        self.ang_v += rad

    def turn_s(self, rad):
        self.field = remake_s(self.field, rad, self.pos)
        self.ang_s += rad

    def move(self, v):
        xp = self.pos[0] + v[0]
        yp = self.pos[1] + v[1]
        zp = self.pos[2] + v[2]
        xf = self.field[0] + v[0]
        yf = self.field[1] + v[1]
        zf = self.field[2] + v[2]
        self.pos = (xp, yp, zp)
        self.field = (xf, yf, zf)


def dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)**0.5


def polygon_center(p1):
    x = 0
    y = 0
    z = 0
    for p in p1:
        x += p[0]
        y += p[1]
        z += p[2]
    x /= len(p1)
    y /= len(p1)
    z /= len(p1)
    return (x, y, z)


def remake_h(p, rad, c):
    x = p[0] - c[0]
    z = (p[1] - c[1]) * sin(rad) + (p[2] - c[2]) * cos(rad)
    y = (p[1] - c[1]) * cos(rad) - (p[2] - c[2]) * sin(rad)
    return (x + c[0], y + c[1], z + c[2])


def remake_v(p, rad, c):
    x = (p[0] - c[0]) * cos(rad) - (p[2] - c[2]) * sin(rad)
    y = p[1] - c[1]
    z = (p[0] - c[0]) * sin(rad) + (p[2] - c[2]) * cos(rad)
    return (x + c[0], y + c[1], z + c[2])


def remake_s(p, rad, c):
    y = (p[1] - c[1]) * cos(rad) - (p[0] - c[0]) * sin(rad)
    z = p[2] - c[2]
    x = (p[1] - c[1]) * sin(rad) + (p[0] - c[0]) * cos(rad)
    return (x + c[0], y + c[1], z + c[2])


def mc(p1, cam):
    ans = []
    for p in p1:
        x = p[0] - cam.pos[0]
        y = p[1] - cam.pos[1]
        z = p[2] - cam.pos[2]
        cur_p = (x, y, z)
        cur_p = remake_h(cur_p, -cam.ang_h, (0, 0, 0))
        cur_p = remake_s(cur_p, -cam.ang_s, (0, 0, 0))
        cur_p = remake_v(cur_p, -cam.ang_v, (0, 0, 0))
        cur_field = (cam.field[0] - cam.pos[0],
                     cam.field[1] - cam.pos[1],
                     cam.field[2] - cam.pos[2])
        cur_field = remake_s(cur_field, -cam.ang_s, (0, 0, 0))
        cur_field = remake_v(cur_field, -cam.ang_v, (0, 0, 0))
        cur_field = remake_h(cur_field, -cam.ang_h, (0, 0, 0))
        if cur_p[2] < 0:
            return [(-1, -1), (-1, -1), (-1, -1), (-1, -1)]
        coefficient = cur_field[2] / cur_p[2]
        x = cur_p[0] * coefficient
        y = cur_p[1] * coefficient
        y = size[1] - y
        ans.append((x + CENTER[0], y - CENTER[1]))
    return ans

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
    p11 = (-100, -100, -100)
    p22 = (-120, -100, -100)
    p33 = (-120, -120, -100)
    p44 = (-100, -120, -100)
    while running:
        pygame.draw.polygon(screen, clr1, mc([p11, p22, p33, p44], camera))
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
        cur_pos = [([p1, p5, p6, p2], dist(camera.pos, polygon_center([p1, p5, p6, p2])), clr1),
                   ([p4, p8, p7, p3], dist(camera.pos, polygon_center([p4, p8, p7, p3])), clr2),
                   ([p1, p5, p8, p4], dist(camera.pos, polygon_center([p1, p5, p8, p4])), clr3),
                   ([p2, p6, p7, p3], dist(camera.pos, polygon_center([p2, p6, p7, p3])), clr4),
                   ([p1, p2, p3, p4], dist(camera.pos, polygon_center([p1, p2, p3, p4])), clr5),
                   ([p5, p6, p7, p8], dist(camera.pos, polygon_center([p5, p6, p7, p8])), clr6)]
        cur_pos.sort(key=lambda x: -x[1])
        pygame.draw.polygon(screen, cur_pos[0][2], mc(cur_pos[0][0], camera))
        pygame.draw.polygon(screen, cur_pos[1][2], mc(cur_pos[1][0], camera))
        pygame.draw.polygon(screen, cur_pos[2][2], mc(cur_pos[2][0], camera))
        pygame.draw.polygon(screen, cur_pos[3][2], mc(cur_pos[3][0], camera))
        pygame.draw.polygon(screen, cur_pos[4][2], mc(cur_pos[4][0], camera))
        pygame.draw.polygon(screen, cur_pos[5][2], mc(cur_pos[5][0], camera))
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
        pygame.time.Clock().tick(30)

