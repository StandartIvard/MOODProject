from py3d import Vector, Camera, mc, polygon_center, remake_h, remake_v, remake_s
import pygame
from py3d import size as screen_size


def manh_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


class Enemy:
    def __init__(self, cords, texture, plane):
        self.cur_position = cords
        self.cords = (self.cur_position[1] * 500, 0, self.cur_position[0] * 500)
        self.texture = texture
        self.path = (0, 0, 0)
        self.plane = plane
        self.next_pos = self.cur_position
        self.size = (texture.get_width, texture.get_height)

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
        pol_c = (pos[0], pos[1] + self.texture.get_height / 2, pos[2])
        cur_p = (pol_c[0] - cam.pos[0], pol_c[1] - cam.pos[1], pol_c[2] - cam.pos[2])
        cur_p = remake_v(cur_p, -cam.ang_v, (0, 0, 0))
        cur_p = remake_h(cur_p, -cam.ang_h, (0, 0, 0))
        cur_p = remake_s(cur_p, -cam.ang_s, (0, 0, 0))
        if mc(pol_c, cam) != (-1, -1):
            coef = cam.cur_field[2] / cur_p[2]
        else:
            return None
        w = Vector(Vector(pos[0]) - Vector(pos[1])).len()
        h = Vector(Vector(pos[0]) - Vector(pos[3])).len()
        w *= coef
        h *= coef
        cur_sprite = pygame.sprite.Sprite()
        cur_sprite.image = pygame.transform.scale(self.texture, (w, h))
        cur_sprite.rect = cur_sprite.image.get_rect()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(cur_sprite)
        all_sprites.update()
