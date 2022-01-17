from math import sin, cos

size = [1400, 800]
CENTER = (size[0] / 2, size[1] / 2, 0)


class Vector:
    def __init__(self, v):
        self.cords = v

    def __mul__(self, other):
        return Vector((self.cords[0] * other, self.cords[1] * other, self.cords[2] * other))

    def __add__(self, other):
        return Vector((self.cords[0] + other.cords[0],
                       self.cords[1] + other.cords[1],
                       self.cords[2] + other.cords[2]))

    def __sub__(self, other):
        return Vector((self.cords[0] - other.cords[0],
                       self.cords[1] - other.cords[1],
                       self.cords[2] - other.cords[2]))

    def __eq__(self, other):
        if self.cords == other.cords:
            return True
        return False

    def __str__(self):
        return "->" + str(self.cords) + "<-"

    def __getitem__(self, item):
        return self.cords[item]

    def len(self):
        return (self.cords[0]**2 + self.cords[1]**2 + self.cords[2]**2)**0.5

    def __abs__(self):
        if self.cords[0] < 0:
            return self * (-1)
        return self


class Camera:
    def __init__(self, pos=(0, 0, 0), field=(0, 0, 1), ang_vert=0, ang_hor=0, ang_st=0):
        self.field = field
        self.pos = pos
        self.ang_v = ang_vert
        self.ang_h = ang_hor
        self.ang_s = ang_st
        self.cur_field = field
        self.cur_field = (self.field[0] - self.pos[0],
                     self.field[1] - self.pos[1],
                     self.field[2] - self.pos[2])
        self.cur_field = remake_s(self.cur_field, -self.ang_s, (0, 0, 0))
        self.cur_field = remake_v(self.cur_field, -self.ang_v, (0, 0, 0))
        self.cur_field = remake_h(self.cur_field, -self.ang_h, (0, 0, 0))
        self.move_vectors = [Vector((0, 0, 100)), Vector((100, 0, 0))]

    def turn_h(self, rad):
        self.field = remake_h(self.field, rad, self.pos)
        self.move_vectors[0] = Vector(remake_h(self.move_vectors[0].cords, rad, (0, 0, 0)))
        self.move_vectors[1] = Vector(remake_h(self.move_vectors[1].cords, rad, (0, 0, 0)))
        self.ang_h += rad

    def turn_v(self, rad):
        self.field = remake_v(self.field, rad, self.pos)
        self.move_vectors[0] = Vector(remake_v(self.move_vectors[0].cords, rad, (0, 0, 0)))
        self.move_vectors[1] = Vector(remake_v(self.move_vectors[1].cords, rad, (0, 0, 0)))
        self.ang_v += rad

    def turn_s(self, rad):
        self.field = remake_s(self.field, rad, self.pos)
        self.move_vectors[0] = Vector(remake_s(self.move_vectors[0].cords, rad, (0, 0, 0)))
        self.move_vectors[1] = Vector(remake_s(self.move_vectors[1].cords, rad, (0, 0, 0)))
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


def is_out(cam, wall, key):
    obj = []
    for p in wall:
        obj.append((p[0] - cam.pos[0], p[1] - cam.pos[1], p[2] - cam.pos[2]))
    if obj[0][0] == obj[1][0]:
        h_point = (obj[0][0], 0, 0)
    else:
        h_point = (0, 0, obj[0][2])
    h_point = remake_h(h_point, -cam.ang_h, (0, 0, 0))
    h_point = remake_v(h_point, -cam.ang_v, (0, 0, 0))
    h_point = remake_s(h_point, -cam.ang_s, (0, 0, 0))
    if key == 'w':
        if h_point[2] < 0:
            return 1
    elif key == 'a':
        if h_point[0] > 0:
            return 1
    elif key == 'd':
        if h_point[0] < 0:
            return 1
    else:
        if h_point[2] > 0:
            return 1
    return 0



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
    pc = []
    for p in p1:
        minus = 0
        x = p[0] - cam.pos[0]
        y = p[1] - cam.pos[1]
        z = p[2] - cam.pos[2]
        cur_p = (x, y, z)
        cur_p = remake_h(cur_p, -cam.ang_h, (0, 0, 0))
        cur_p = remake_s(cur_p, -cam.ang_s, (0, 0, 0))
        cur_p = remake_v(cur_p, -cam.ang_v, (0, 0, 0))
        cur_field = cam.cur_field
        if cur_p[2] < 0 or dist(cur_p, (0, 0, 0)) < 10:
            return [(1, 1), (1, 1), (1, 1), (1, 1)]
        try:
            coefficient = cur_field[2] / cur_p[2]
        except ZeroDivisionError:
            return [(1, 1), (1, 1), (1, 1), (1, 1)]
        x = cur_p[0] * coefficient
        y = cur_p[1] * coefficient
        pc.append((x, y, 0))
        y = size[1] - y
        ans.append((x + CENTER[0], y - CENTER[1]))
    if dist(polygon_center(pc), (0, 0, 0)) > (2**0.5) * 1000:
        return [(1, 1), (1, 1), (1, 1), (1, 1)]
    return ans