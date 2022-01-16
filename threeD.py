import pygame
from math import pi
from py3d import Camera, size, remake_s, remake_h, remake_v, dist, polygon_center, mc, Vector, is_out
from math import pi, sin, cos
from time import time
import sys
from funcForMap import translateMap
from loadImage import load_hand_image


class Game:
    pause = False
    qtacess = False
    h = 50
    shooting = False
    count = 0
    indx = 1

    playlist = [
        './data/sounds/METALMUSICONE.wav',
        './data/sounds/METALMUSICTWO.wav'
    ]

    pygame.mixer.init()
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('./data/sounds/METALMUSICONE.wav'))
    pygame.mixer.Channel(0).set_volume(0.5)
    pygame.mixer.Channel(0).queue(pygame.mixer.Sound('./data/sounds/METALMUSICTWO.wav'))

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
        self.camera = Camera((2000, 800, -(3**0.5) * 200 + 1500), (2000, 800, 1500))
        self.terrain = []
        self.tecmap = 'mapName'
        self.clr3 = pygame.Color((27, 0, 0))
        cur_map = translateMap(self.tecmap, self.camera, self.clr3)
        self.plane_map = []
        self.plane_map.extend(cur_map)
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

        self.sprites_of_hands_1 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/NormalHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_1.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.sprites_of_hands_2 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/SecondHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_2.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.sprites_of_hands_3 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/ThirdHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_3.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.sprites_of_hands_4 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/FourthHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_4.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.sprites_of_hands_5 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/FithHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_5.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.sprites_of_hands_6 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/SixthHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_6.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.sprites_of_hands_7 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/SeventhHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_7.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.sprites_of_hands_8 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/EighthHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_8.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.scope = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/scope.png")
        sprite.rect = sprite.image.get_rect()
        self.scope.add(sprite)
        sprite.rect.x = 0
        sprite.rect.y = 0

        self.handGroups = [self.sprites_of_hands_1, self.sprites_of_hands_2, self.sprites_of_hands_3,
                           self.sprites_of_hands_4, self.sprites_of_hands_5, self.sprites_of_hands_6,
                           self.sprites_of_hands_7, self.sprites_of_hands_8, self.sprites_of_hands_7,
                           self.sprites_of_hands_6, self.sprites_of_hands_5, self.sprites_of_hands_4,
                           self.sprites_of_hands_2, self.sprites_of_hands_1]
        print(len(self.plane_map))

    def main_loop(self, window):
        if self.qtacess:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if not self.shooting:
                    self.shooting = True
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound('./data/sounds/ShootingSound.wav'))

            if keys[pygame.K_w]:
                my_v = self.camera.move_vectors[0]
                result_v = my_v
                for v in self.stuck_polygons:
                    if len(self.stuck_polygons) > 1:
                        if is_out(self.camera, self.stuck_polygons[0], 'w') == 1 and is_out(self.camera, self.stuck_polygons[0], 'w') == 1:
                            break
                        else:
                            result_v = Vector((0, 0, 0))
                    if is_out(self.camera, v, 'w'):
                        continue
                    result_v = Vector((0, 0, 0))
                    if v[0][0] == v[1][0]:
                        ang = -(pi / 2) + self.camera.ang_v
                    else:
                        ang = self.camera.ang_v
                    buffer_vector = Vector(v[0]) - Vector(v[1])
                    vector = buffer_vector * (1 / buffer_vector.len())
                    result_v = result_v + vector * sin(ang) * my_v.len()
                self.camera.move(result_v.cords)
            if keys[pygame.K_a]:
                my_v = self.camera.move_vectors[1] * (-1)
                result_v = my_v
                for v in self.stuck_polygons:
                    if is_out(self.camera, v, 'a'):
                        continue
                    result_v = Vector((0, 0, 0))
                    if v[0][0] == v[1][0]:
                        ang = self.camera.ang_v
                    else:
                        ang = self.camera.ang_v + (pi / 2)
                    buffer_vector = Vector(v[0]) - Vector(v[1])
                    vector = buffer_vector * (1 / buffer_vector.len())
                    result_v = result_v + vector * sin(ang) * my_v.len()
                self.camera.move(result_v.cords)
            if keys[pygame.K_d]:
                my_v = self.camera.move_vectors[1]
                result_v = my_v
                for v in self.stuck_polygons:
                    if is_out(self.camera, v, 'd'):
                        continue
                    result_v = Vector((0, 0, 0))
                    if v[0][0] == v[1][0]:
                        ang = -self.camera.ang_v
                    else:
                        ang = -self.camera.ang_v - (pi / 2)
                    buffer_vector = Vector(v[0]) - Vector(v[1])
                    vector = buffer_vector * (1 / buffer_vector.len())
                    result_v = result_v + vector * sin(ang) * my_v.len()
                self.camera.move(result_v.cords)
            if keys[pygame.K_s]:
                my_v = self.camera.move_vectors[0] * (-1)
                result_v = my_v
                for v in self.stuck_polygons:
                    if is_out(self.camera, v, 's'):
                        continue
                    result_v = Vector((0, 0, 0))
                    if v[0][0] == v[1][0]:
                        ang = (pi / 2) + self.camera.ang_v
                    else:
                        ang = self.camera.ang_v + pi
                    buffer_vector = Vector(v[0]) - Vector(v[1])
                    vector = buffer_vector * (1 / buffer_vector.len())
                    result_v = result_v + vector * sin(ang) * my_v.len()
                self.camera.move(result_v.cords)
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
                cur_vector = abs(Vector(Vector(point[0][0]) - Vector(point[0][1])))
                if point[0][0][1] == point[0][2][1]:
                    plane_dist = 600
                elif point[0][0][0] == point[0][1][0]:
                    if point[0][0][2] >= self.camera.pos[2] >= point[0][1][2] or point[0][0][2] <= self.camera.pos[2] <= point[0][1][2]:
                        plane_dist = abs(point[0][0][0] - self.camera.pos[0])
                    else:
                        plane_dist = 600
                elif point[0][0][2] == point[0][1][2]:
                    if point[0][0][0] >= self.camera.pos[0] >= point[0][1][0] or point[0][0][0] <= self.camera.pos[0] <= point[0][1][0]:
                        plane_dist = abs(point[0][0][2] - self.camera.pos[2])
                    else:
                        plane_dist = 600
                else:
                    plane_dist = 600
                cur_color.hsva = (cur_color.hsva[0], cur_color.hsva[1],
                                  max(0.01, min(1, 400 / cur_dist)) * 100,
                                  cur_color.hsva[3])
                self.hole_points[ind] = (self.hole_points[ind][0], cur_dist, cur_color)
                if plane_dist < 575:
                    try:
                        if self.stuck_polygons[0] != cur_vector and self.stuck_polygons[1] != cur_vector:
                            self.stuck_polygons.append(point[0])
                    except Exception:
                        self.stuck_polygons.append(point[0])
                square = mc(point[0], self.camera)
                if square != [(1, 1), (1, 1), (1, 1), (1, 1)]:
                    pygame.draw.polygon(self.screen, point[2], square)
            pygame.draw.circle(self.screen, pygame.Color('red'), mc([(0, 0, 0)], self.camera)[0], 5)

            if self.shooting:
                if self.count == 13:
                    self.count = 0
                    self.shooting = False
                else:
                    self.count += self.indx

            self.handGroups[self.count].draw(self.screen)
            self.scope.draw(self.screen)

            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            pygame.time.Clock().tick(100)
            return False
