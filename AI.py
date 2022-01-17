from py3d import Vector, remake_v, remake_h, remake_s, Camera


def manh_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Enemy:
    def __init__(self, cords, texture, plane):
        self.cur_position = cords
        self.cords = (self.cur_position[1] * 500, 0, self.cur_position[0] * 500)
        self.texture = texture
        self.path = (0, 0, 0)
        self.plane = plane

    def find_path(self, target):
        try:
            k = (self.cur_position[1] - target.cur_position[1]) / (self.cur_position[0] - target.cur_position[0])
            if (self.cur_position[0] < target.cur_position[0] and k < 0):
                next_pos = (self.cur_position[0] + 1, self.cur_position[1] + 1)
            elif (self.cur_position[0] < target.cur_position[0] and k > 0):
                next_pos = (self.cur_position[0] + 1, self.cur_position[1] - 1)
            elif (self.cur_position[0] > target.cur_position[0] and k < 0):
                next_pos = (self.cur_position[0] - 1, self.cur_position[1] + 1)
            elif (self.cur_position[0] > target.cur_position[0] and k > 0):
                next_pos = (self.cur_position[0] - 1, self.cur_position[1] - 1)
            elif k == 0 and self.cur_position[0] > target.cur_position[0]:
                next_pos = (self.cur_position[0] - 1, self.cur_position[1])
            else:
                next_pos = (self.cur_position[0] + 1, self.cur_position[1])
        except ZeroDivisionError:
            if self.cur_position[1] > target.cur_position[1]:
                next_pos = (self.cur_position[0] - 1, self.cur_position[1])
            else:
                next_pos = (self.cur_position[0] + 1, self.cur_position[1])
        if self.plane[next_pos[0]][next_pos[1]] != 0:
            next_pos = (10000, 10000)
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if self.plane[self.cur_position[0] + i][self.cur_position[1] + j] == 0 and manh_dist(target.cur_position, (self.cur_position[0] + i, self.cur_position[1] + j)) < manh_dist(next_pos, target.cur_position):
                        next_pos = (self.cur_position[0] + i, self.cur_position[1] + j)
        return next_pos