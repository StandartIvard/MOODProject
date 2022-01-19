from py3d import Vector, Camera, mc, polygon_center
import pygame


def manh_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Enemy:
    def __init__(self, cords, texture, plane, size):
        self.cur_position = cords
        self.cords = (self.cur_position[1] * 500, 0, self.cur_position[0] * 500)
        self.texture = texture
        self.path = (0, 0, 0)
        self.plane = plane
        self.next_pos = self.cur_position
        self.size = size

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
        self.next_pos = next_pos

    def move(self):
        v1 = Vector((self.next_pos[0], 0, self.next_pos[1]))
        v2 = Vector((self.cur_position[0], 0, self.cur_position[1]))
        mv = Vector(v1 - v2) * 100
        self.cords = (self.cords[0] - mv[0], self.cords[1] - mv[1], self.cords[2] - mv[2])
        if self.next_pos[0] * 500 <= self.cords[2] <= self.next_pos[0] * 500 + 500:
            if self.next_pos[1] * 500 <= self.cords[0] <= self.next_pos[1] * 500 + 500:
                self.cur_position = self.next_pos

    def draw(self, pos, cam):
        stand_point = ((pos[2][0] - pos[3][0]) / 2, 0, (pos[2][2] - pos[3][2]) / 2)
        surf_pos = mc(stand_point, cam)
        sc = (surf_pos[0] - self.texture.get_width / 2, surf_pos[1] - self.texture.get_height)
