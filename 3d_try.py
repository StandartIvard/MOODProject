import pygame
from math import sin, cos

CENTER = (150, 150, round((3**0.5) * 150))

def dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)**0.5

def remake_h(p, rad, c):
    x = p[0] - c[0]
    z = (p[1] - c[1]) * sin(rad) + (p[2] - c[2]) * cos(rad)
    y = (p[1] - c[1]) * cos(rad) - (p[2] - c[2]) * sin(rad)
    return (round(x + c[0]), round(y + c[1]), round(z + c[2]))

def remake_v(p, rad, c):
    x = (p[0] - c[0]) * cos(rad) - (p[2] - c[2]) * sin(rad)
    z = (p[0] - c[0]) * sin(rad) + (p[2] - c[2]) * cos(rad)
    y = p[1] - c[1]
    return (round(x + c[0]), round(y + c[1]), round(z + c[2]))

def mc(p1):
    ans = []
    for p in p1:
        x = (p[0] * CENTER[2]) / p[2]
        y = (p[1] * CENTER[2]) / p[2]
        x += CENTER[0]
        y += CENTER[1]
        ans.append((round(x), round(y)))
    return ans

if __name__ == '__main__':
    w = 0.05
    h = 50
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
    size = 300, 300
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        cur_pos = [([p1, p5, p6, p2], (p1[2] + p5[2] + p6[2] + p2[2]) / 4, clr1),
                   ([p4, p8, p7, p3], (p4[2] + p8[2] + p7[2] + p3[2]) / 4, clr2),
                   ([p1, p5, p8, p4], (p1[2] + p5[2] + p8[2] + p4[2]) / 4, clr3),
                   ([p2, p6, p7, p3], (p2[2] + p6[2] + p7[2] + p3[2]) / 4, clr4),
                   ([p1, p2, p3, p4], (p1[2] + p2[2] + p3[2] + p4[2]) / 4, clr5),
                   ([p5, p6, p7, p8], (p5[2] + p6[2] + p7[2] + p8[2]) / 4, clr6)]
        cur_pos.sort(key=lambda x: x[1])
        pygame.draw.polygon(screen, cur_pos[0][2], mc(cur_pos[0][0]))
        pygame.draw.polygon(screen, cur_pos[1][2], mc(cur_pos[1][0]))
        pygame.draw.polygon(screen, cur_pos[2][2], mc(cur_pos[2][0]))
        pygame.draw.polygon(screen, cur_pos[3][2], mc(cur_pos[3][0]))
        pygame.draw.polygon(screen, cur_pos[4][2], mc(cur_pos[4][0]))
        pygame.draw.polygon(screen, cur_pos[5][2], mc(cur_pos[5][0]))
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
        p1 = remake_h(p1, w, (h / 2, p1[1], h / 2))
        p2 = remake_h(p2, w, (h / 2, p2[1], h / 2))
        p3 = remake_h(p3, w, (h / 2, p3[1], h / 2))
        p4 = remake_h(p4, w, (h / 2, p4[1], h / 2))
        p5 = remake_h(p5, w, (h / 2, p5[1], h / 2))
        p6 = remake_h(p6, w, (h / 2, p6[1], h / 2))
        p7 = remake_h(p7, w, (h / 2, p7[1], h / 2))
        p8 = remake_h(p8, w, (h / 2, p8[1], h / 2))
        pygame.time.Clock().tick(30)

