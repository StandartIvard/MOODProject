from py3d import Vector, Camera, mc, polygon_center, remake_h, remake_v, remake_s
import pygame
from py3d import size as screen_size


def manh_dist(p1, p2):
    m = min(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
    return m * 1.41 + max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1])) - m


class Enemy:
    def __init__(self, cords, texture, plane):
        self.cur_position = cords
        self.cords = (self.cur_position[1] * 500, 0, self.cur_position[0] * 500)
        self.texture = texture
        self.path = (0, 0, 0)
        self.plane = plane
        self.next_pos = self.cur_position
        self.size = texture.get_rect().size

    def find_path(self, target):
        next_pos = (10000, 10000)
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                next_cords = (self.cords[0] + i * 50, 0, self.cords[2] + j * 50)
                if self.plane[next_cords[2] // 500][next_cords[0] // 500] == 0:
                    if manh_dist(target.cur_position, (self.cur_position[0] + i, self.cur_position[1] + j)) < manh_dist(next_pos, target.cur_position):
                            next_pos = (self.cur_position[0] + i, self.cur_position[1] + j)
        self.next_pos = next_pos
        print(target.cur_position)

    def move(self):
        v1 = Vector((self.next_pos[1], 0, self.next_pos[0]))
        v2 = Vector((self.cur_position[1], 0, self.cur_position[0]))
        mv = Vector(v1 - v2) * 25
        self.cords = (self.cords[0] + mv[0], self.cords[1] + mv[1], self.cords[2] + mv[2])
        self.cur_position = (self.cords[2] // 500, self.cords[0] // 500)
        """if self.next_pos[0] * 500 <= self.cords[2] <= self.next_pos[0] * 500 + 500:
            if self.next_pos[1] * 500 <= self.cords[0] <= self.next_pos[1] * 500 + 500:
                self.cur_position = self.next_pos"""
        #self.plane[self.cur_position[0]][self.cur_position[1]] = -1
        print(self.next_pos, self.cur_position, self.cords)

    def draw(self, pos, cam, screen):
        pol_c = (pos[0], pos[1] + self.texture.get_height() / 2, pos[2])
        if mc(pol_c, cam) == (-1, -1):
            return None
        cur_p = (pol_c[0] - cam.pos[0], pol_c[1] - cam.pos[1], pol_c[2] - cam.pos[2])
        cur_p = remake_v(cur_p, -cam.ang_v, (0, 0, 0))
        cur_p = remake_h(cur_p, -cam.ang_h, (0, 0, 0))
        cur_p = remake_s(cur_p, -cam.ang_s, (0, 0, 0))
        if mc(pol_c, cam) != (-1, -1):
            coef = cam.cur_field[2] / cur_p[2]
        else:
            return None
        w = self.texture.get_width()
        h = self.texture.get_height()
        w *= coef
        h *= coef
        screen_p = mc(pol_c, cam)
        cur_sprite = pygame.sprite.Sprite()
        cur_sprite.image = pygame.transform.scale(self.texture, (w, h))
        cur_sprite.rect = cur_sprite.image.get_rect()
        cur_sprite.rect.x = screen_p[0] - cur_sprite.image.get_width() / 2
        cur_sprite.rect.y = screen_p[1] - cur_sprite.image.get_height() / 2
        group = pygame.sprite.Group()
        group.add(cur_sprite)
        group.draw(screen)
