from math import sin, cos

size = [600, 600]
CENTER = (size[0] / 2, size[1] / 2, 0)


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
        """if z < 0:
            ans = [(-1, -1), (-1, -1), (-1, -1), (-1, -1)]
            break"""
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
        coefficient = cur_field[2] / cur_p[2]
        x = cur_p[0] * coefficient
        y = cur_p[1] * coefficient
        y = size[1] - y
        ans.append((x + CENTER[0], y - CENTER[1]))
    return ans