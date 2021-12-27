from py3d import polygon_center, dist


def translateMap(name, cam, color):
    f = open('./data/maps/' + name + '.txt')
    map = f.readlines()
    cords = list()
    c = 50
                                            #  (int(map[i][j]), i, (len(map[i]) - j) - 1)
    for i in range(len(map) - 1):
        map[i] = ''.join(map[i].split())
        map[i + 1] = ''.join(map[i + 1].split())
        for j in range(len(map[i]) - 1):
            if map[i][j] == map[i][j + 1] == map[i + 1][j] == map[i + 1][j + 1] and int(map[i][j]) != 0:
                temp = polygon_center([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                                (len(map[i + 1]) - j, int(map[i + 1][j]), i + 1),
                                 (len(map[i + 1]) - j - 1, int(map[i + 1][j]), i + 1)])
                cords.append([[(c * (len(map[i]) - j - 1), c * int(map[i][j]), c * i), (c * (len(map[i]) - j), c * int(map[i][j + 1]), c * i),
                                (c * len(map[i + 1]) - j, c * int(map[i + 1][j]), (i + 1) * c),
                                 (c * (len(map[i + 1]) - j - 1), c * int(map[i + 1][j]), (i + 1) * c)],
                                 dist(temp, cam.pos), color])
            elif map[i][j] != map[i + 1][j + 1] and int(map[i][j]) != 0:
                if map[i][j] == map[i][j + 1]:
                    temp = polygon_center([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                                     (len(map[i]) - j, 0, i), (len(map[i]) - j - 1, 0, i)])
                    cords.append([[((len(map[i]) - j - 1) * c, c * int(map[i][j]), c * i), ((len(map[i]) - j) * c, c * int(map[i][j + 1]), c * i),
                                     ((len(map[i]) - j) * c, 0, c * i), (c * (len(map[i]) - j - 1), 0, c * i)],
                                     dist(temp, cam.pos), color])
                if map[i][j] == map[i + 1][j]:
                    temp = polygon_center([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i + 1]) - j, int(map[i][j]), i),
                                     (len(map[i + 1]) - j, 0, i), (len(map[i]) - j - 1, 0, i)])
                    cords.append([[((len(map[i]) - j - 1) * c, c * int(map[i][j]), c * i), ((len(map[i + 1]) - j) * c, c * int(map[i][j]), c * i),
                                     ((len(map[i + 1]) - j) * c, 0, c * i), ((len(map[i]) - j - 1) * c, 0, c * i)],
                                     dist(temp, cam.pos), color])
    i = len(map) - 2
    for j in range(len(map[i]) - 1):
        if map[i][j] == map[i][j + 1] and int(map[i][j]) != 0:
            temp = polygon_center([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                    (len(map[i]) - j, 0, i), (len(map[i]) - j - 1, 0, i)])
            cords.append([[((len(map[i]) - j - 1) * c, c * int(map[i][j]), c * i), ((len(map[i]) - j) * c, c * int(map[i][j + 1]), c * i),
                             ((len(map[i]) - j) * c, 0, c * i), ((len(map[i]) - j - 1) * c, 0, c * i)],
                             dist(temp, cam.pos), color])
    return cords