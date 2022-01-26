import pygame
from math import pi
from py3d import Camera, size, remake_s, remake_h, remake_v, dist, polygon_center, mc,\
    Vector, is_out, find_angle, is_inside
from math import pi, sin, cos
from time import time
import sys
from funcForWorkWithDB import updateHP
from funcForMap import translateMap, create_map
from loadImage import load_hand_image, load_enemy_image
from AI import Enemy


class Game:
    pause = False
    qtacess = False
    h = 50
    shooting = False
    count = 0
    indx = 1
    name = ''
    dead = False

    playlist = [
        './data/sounds/METALMUSICONE.wav',
        './data/sounds/METALMUSICTWO.wav'
    ]

    pygame.mixer.init()
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('./data/sounds/METALMUSICONE.wav'))
    pygame.mixer.Channel(0).set_volume(0)
    pygame.mixer.Channel(0).queue(pygame.mixer.Sound('./data/sounds/METALMUSICTWO.wav'))

    def __init__(self):
        pygame.init()
        self.game_init()

    def game_init(self):
        print('11')
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
        self.damage = 25
        self.screen = pygame.display.set_mode((0, 0))
        W, H = self.screen.get_size()
        self.screen = pygame.display.set_mode((W, H))
        global size
        size = (W, H)

        self.HP = 100
        self.score = 0

        self.LR = (W - 900) // 2
        self.UD = (H - 600) // 2

        self.screen.fill((0, 0, 0))
        self.running = True
        self.camera = Camera((2000, 800, -(3**0.5) * 200 + 1500), (2000, 800, 1500))
        self.terrain = []
        self.tecmap = 'mapName'
        self.clr3 = pygame.Color((27, 0, 0))
        cur_map = translateMap(self.tecmap, self.camera, self.clr3)
        self.plane_map = []
        self.plane_map.extend(cur_map)

        self.hole_points = []
        # self.hole_points.extend(self.cube)
        self.hole_points.extend(self.plane_map)

        self.stuck_polygons = []
        self.din_map = create_map(self.tecmap)
        self.din_map[6][4] = -1
        self.din_map[6][12] = -2
        im1 = load_enemy_image('data/images/enemys/enemy_move_1.png')
        im2 = load_enemy_image('data/images/enemys/enemy_move_2.png')
        im3r = load_enemy_image('data/images/enemys/enemy_move_3.png')
        im4r = load_enemy_image('data/images/enemys/enemy_move_4.png')
        im3 = load_enemy_image('data/images/enemys/enemy_move_5.png')
        im4 = load_enemy_image('data/images/enemys/enemy_move_6.png')
        im5 = load_enemy_image('data/images/enemys/enemy_move_7.png')
        im6 = load_enemy_image('data/images/enemys/enemy_move_1_2.png')
        im7 = load_enemy_image('data/images/enemys/enemy_move_2_1.png')
        im8 = load_enemy_image('data/images/enemys/enemy_move_3_1.png')
        im9 = load_enemy_image('data/images/enemys/enemy_move_4_1.png')
        im6r = load_enemy_image('data/images/enemys/enemy_move_1_2_r.png')
        im7r = load_enemy_image('data/images/enemys/enemy_move_2_1_r.png')
        im8r = load_enemy_image('data/images/enemys/enemy_move_3_1_r.png')
        im9r = load_enemy_image('data/images/enemys/enemy_move_4_1_r.png')
        im10 = load_enemy_image('data/images/enemys/enemy_move_1_3.png')
        im11 = load_enemy_image('data/images/enemys/enemy_move_2_2.png')
        im12 = load_enemy_image('data/images/enemys/enemy_move_3_2.png')
        im13 = load_enemy_image('data/images/enemys/enemy_move_4_2.png')
        im10r = load_enemy_image('data/images/enemys/enemy_move_1_3_r.png')
        im11r = load_enemy_image('data/images/enemys/enemy_move_2_2_r.png')
        im12r = load_enemy_image('data/images/enemys/enemy_move_3_2_r.png')
        im13r = load_enemy_image('data/images/enemys/enemy_move_4_2_r.png')
        im1d = load_enemy_image('data/images/enemys/death_1.png')
        im2d = load_enemy_image('data/images/enemys/death_2.png')
        im3d = load_enemy_image('data/images/enemys/death_3.png')
        im4d = load_enemy_image('data/images/enemys/death_4.png')
        im5d = load_enemy_image('data/images/enemys/death_5.png')
        self.test_monster1 = Enemy((6, 4), [[im5], [im3, im4, im5],
                                            [im1, im2, im3r, im4r],
                                            [im6, im7, im8, im9],
                                            [im6r, im7r, im8r, im9r],
                                            [im10, im11, im12, im13],
                                            [im10r, im11r, im12r, im13r],
                                            [im1d, im2d, im3d, im4d, im5d]], self.din_map, -1)
        self.hole_points.append([self.test_monster1.cords, 10000, self.test_monster1, 1])
        self.test_monster2 = Enemy((6, 12), [[im5], [im3, im4, im5],
                                            [im1, im2, im3r, im4r],
                                            [im6, im7, im8, im9],
                                            [im6r, im7r, im8r, im9r],
                                            [im10, im11, im12, im13],
                                            [im10r, im11r, im12r, im13r],
                                            [im1d, im2d, im3d, im4d, im5d]], self.din_map, -2)
        self.hole_points.append([self.test_monster2.cords, 10000, self.test_monster2, 1])

        cm = create_map(self.tecmap)
        for i in range(len(cm)):
            for j in range(len(cm[i])):
                if 0 < i < len(cm) - 1 and 0 < j < len(cm[i]) - 1 and cm[i][j] != 0:
                    print((i, j))
        self.current_target = self.hole_points[0]
        self.sprites_of_hands_1 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/NormalHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_1.add(sprite)
        sprite.rect.x = self.LR - 20
        sprite.rect.y = self.UD - 40

        self.sprites_of_hands_2 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/SecondHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_2.add(sprite)
        sprite.rect.x = self.LR - 20
        sprite.rect.y = self.UD - 40

        self.sprites_of_hands_3 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/ThirdHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_3.add(sprite)
        sprite.rect.x = self.LR - 20
        sprite.rect.y = self.UD - 40

        self.sprites_of_hands_4 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/FourthHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_4.add(sprite)
        sprite.rect.x = self.LR - 20
        sprite.rect.y = self.UD - 40

        self.sprites_of_hands_5 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/FithHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_5.add(sprite)
        sprite.rect.x = self.LR - 20
        sprite.rect.y = self.UD - 40

        self.sprites_of_hands_6 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/SixthHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_6.add(sprite)
        sprite.rect.x = self.LR - 20
        sprite.rect.y = self.UD - 40

        self.sprites_of_hands_7 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/SeventhHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_7.add(sprite)
        sprite.rect.x = self.LR - 20
        sprite.rect.y = self.UD - 40

        self.sprites_of_hands_8 = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/HandSprites/EighthHands.png")
        sprite.rect = sprite.image.get_rect()
        self.sprites_of_hands_8.add(sprite)
        sprite.rect.x = self.LR - 20
        sprite.rect.y = self.UD - 40

        self.scope = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/scope.png")
        sprite.rect = sprite.image.get_rect()
        self.scope.add(sprite)
        sprite.rect.x = self.LR
        sprite.rect.y = self.UD + 100

        self.sides = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = load_hand_image("data/images/sides1.png")
        sprite.rect = sprite.image.get_rect()
        self.scope.add(sprite)
        sprite.rect.x = -1 * (510 - self.LR)
        sprite.rect.y = -1 * (240 - self.UD + 50)

        self.handGroups = [self.sprites_of_hands_1, self.sprites_of_hands_2, self.sprites_of_hands_3,
                           self.sprites_of_hands_4, self.sprites_of_hands_5, self.sprites_of_hands_6,
                           self.sprites_of_hands_7, self.sprites_of_hands_8, self.sprites_of_hands_7,
                           self.sprites_of_hands_6, self.sprites_of_hands_5, self.sprites_of_hands_4,
                           self.sprites_of_hands_2, self.sprites_of_hands_1]
        print(len(self.plane_map))

    def draw_te(self, surf, text, size, x, y):
        font_name = pygame.font.match_font('arial')
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, pygame.Color((255, 255, 255)))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def main_loop(self, window):
        if self.qtacess:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if not self.shooting:
                    self.shooting = True
                    if self.current_target[3] == 1:
                        self.current_target[2].hitpoints -= self.damage
                        self.current_target[2].texture = self.current_target[2].death_run[0]
                        self.current_target[2].stunned = 1
                        if self.current_target[2].hitpoints <= 0 and self.current_target[2].hitpoints + self.damage > 0:
                            self.current_target[2].death = True
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
                self.camera.turn_v(pi / 12)
            if keys[pygame.K_RIGHT]:
                self.camera.turn_v(-pi / 12)
            if keys[pygame.K_ESCAPE]:
                self.qtacess = False
                self.pause = True
            self.hole_points.sort(key=lambda x: -x[1])
            self.stuck_polygons = []
            for point in self.hole_points:
                ind = self.hole_points.index(point)
                if point[3] == 0:
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
                    self.hole_points[ind] = [self.hole_points[ind][0], cur_dist, cur_color, 0]
                    if plane_dist < 575:
                        try:
                            if self.stuck_polygons[0] != cur_vector and self.stuck_polygons[1] != cur_vector:
                                self.stuck_polygons.append(point[0])
                        except Exception:
                            self.stuck_polygons.append(point[0])
                    square = mc(point[0], self.camera)
                    if square != [(1, 1), (1, 1), (1, 1), (1, 1)]:
                        if is_inside(square, (450, 300)) == True:
                            self.current_target = point
                        pygame.draw.polygon(self.screen, point[2], square)
                else:
                    point[2].plane = self.din_map
                    cur_dist = dist(point[0], self.camera.pos)
                    self.hole_points[ind][1] = cur_dist
                    if point[2].death == True:
                        point[2].death_count += 1
                        point[2].texture = point[2].death_run[point[2].death_count]
                    if point[2].death_count >= 4:
                        point[2].death = False
                    point[2].draw(point[0], self.camera, self.screen)
                    if point[2].hitpoints <= 0:
                        continue
                    if 0 < point[2].stunned < 4:
                        point[2].stunned += 1
                        continue
                    else:
                        point[2].stunned = 0
                    cam_pos = (self.camera.pos[0], 0, self.camera.pos[2])
                    if dist(cam_pos, point[2].cords) > 900:
                        point[2].hitting = False
                    elif point[2].hit_count >= len(point[2].hit_textures) * 2:
                        point[2].hitting = False
                    else:
                        point[2].hitting = True
                    if point[2].hitting == True:
                        point[2].texture = point[2].hit_textures[point[2].hit_count // 2]
                        point[2].hit_count += 1
                    else:
                        point[2].run_count += 1
                        point[2].run_count %= 3 * len(point[2].run_texture)
                        point[2].texture = point[2].run_texture[point[2].run_count // 3]
                        point[2].find_path(self.camera)
                        point[2].move()
                        this_ang = find_angle(point[2].cords, point[2].lp, self.camera)
                        if this_ang < pi / 6:
                            point[2].run_texture = point[2].r_90_run
                        elif this_ang < pi / 3:
                            point[2].run_texture = point[2].r_45_run
                        elif this_ang < 2 * pi / 3:
                            point[2].run_texture = point[2].f_run
                        elif this_ang < 5 * pi / 6:
                            point[2].run_texture = point[2].l_45_run
                        elif this_ang == 10:
                            point[2].run_texture = point[2].stop_run
                        else:
                            point[2].run_texture = point[2].l_90_run
                        point[2].hit_count = 0
                    if point[2].hit_count >= len(point[2].hit_textures) / 2:
                        self.HP -= 10
                    point[0] = point[2].cords
                    self.din_map = point[2].plane
                    screen_pos = mc(point[2].cords, self.camera)
                    if size[0] // 2 - 100 <= screen_pos[0] <= size[0] // 2 + 100:
                        self.current_target = point
            if self.shooting:
                if self.count == 13:
                    self.count = 0
                    self.shooting = False
                else:
                    self.count += self.indx
            self.HP = max(self.HP, 0)
            updateHP(self.name, self.HP)
            if self.HP == 0:
                self.dead = True
            self.handGroups[self.count].draw(self.screen)
            self.scope.draw(self.screen)
            #            ---------------------------------------------------------------
            #                       INTERFACE
            #            ---------------------------------------------------------------

                                  #  UPPER POLYGON
            #pygame.draw.polygon(self.screen, pygame.Color((26, 26, 26)), [(0, 0), (size[0], 0), (size[0], self.UD - 50), (0, self.UD - 50)])

                                  #  LOWER POLYGON
            #pygame.draw.polygon(self.screen, pygame.Color((26, 26, 26)), [(0, size[1]), (0, size[1] - self.UD - 50), (size[0], size[1] - self.UD - 50), (size[0], size[1])])

                                  #  LEFT POLYGON
            #pygame.draw.polygon(self.screen, pygame.Color((26, 26, 26)), [(0, 0), (self.LR, 0), (self.LR, size[1]), (0, size[1])])

                                  #  RIGHT POLYGON
            #pygame.draw.polygon(self.screen, pygame.Color((26, 26, 26)), [(size[0], 0), (size[0] - self.LR, 0), (size[0] - self.LR, size[1]), (size[0], size[1])])

                                  #  HP UNDERBAR
            pygame.draw.polygon(self.screen, pygame.Color((100, 100, 100)), [(size[0] // 20, size[1] - self.UD - 20), (size[0] // 2, size[1] - self.UD - 20), (size[0] // 2, size[1] - (self.UD + 20) // 2), (size[0] // 20, size[1] - (self.UD + 20) // 2)])

            size_x = size[0] // 2 - size[0] // 20

                                  #  HP BAR
            pygame.draw.polygon(self.screen, pygame.Color((0, 255, 0)), [(size[0] // 20, size[1] - self.UD - 20), ((size_x / 100) * self.HP + size[0] // 20, size[1] - self.UD - 20), ((size_x / 100) * self.HP + size[0] // 20, size[1] - (self.UD + 20) // 2), (size[0] // 20, size[1] - (self.UD + 20) // 2)])

                                  #  score
            self.draw_te(self.screen, str(self.score), 100, (size[0] / 2) + size[0] / 5, size[1] - self.UD - 20)

            self.sides.draw(self.screen)

            pygame.display.flip()
            self.screen.fill((0, 0, 0))
            pygame.time.Clock().tick(100)

            return False