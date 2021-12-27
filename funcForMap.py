from py3d import polygon_center, dist


def translateMap(name, cam, color):
    f = open('./data/maps/' + name + '.txt')
    map = f.readlines()
    cords = list()
                                            #  (int(map[i][j]), i, (len(map[i]) - j) - 1)
    for i in range(len(map) - 1):
        cords.append([])
        map[i] = ''.join(map[i].split())
        map[i + 1] = ''.join(map[i + 1].split())
        for j in range(len(map[i]) - 1):
            if map[i][j] == map[i][j + 1] == map[i + 1][j] == map[i + 1][j + 1] and int(map[i][j]) != 0:
                temp = polygon_center([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                                (len(map[i + 1]) - j, int(map[i + 1][j]), i + 1),
                                 (len(map[i + 1]) - j - 1, int(map[i + 1][j]), i + 1)])
                cords[i].append([[(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                                (len(map[i + 1]) - j, int(map[i + 1][j]), i + 1),
                                 (len(map[i + 1]) - j - 1, int(map[i + 1][j]), i + 1)],
                                 color, dist(temp, cam.pos)])
            elif map[i][j] != map[i + 1][j + 1] and int(map[i][j]) != 0:
                if map[i][j] == map[i][j + 1]:
                    temp = polygon_center([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                                     (len(map[i]) - j, 0, i), (len(map[i]) - j - 1, 0, i)])
                    cords[i].append([[(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                                     (len(map[i]) - j, 0, i), (len(map[i]) - j - 1, 0, i)],
                                     color, dist(temp, cam.pos)])
                if map[i][j] == map[i + 1][j]:
                    temp = polygon_center([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i + 1]) - j, int(map[i][j]), i),
                                     (len(map[i + 1]) - j, 0, i), (len(map[i]) - j - 1, 0, i)])
                    cords[i].append([[(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i + 1]) - j, int(map[i][j]), i),
                                     (len(map[i + 1]) - j, 0, i), (len(map[i]) - j - 1, 0, i)],
                                     color, dist(temp, cam.pos)])
    i = len(map) - 2
    cords.append([])
    for j in range(len(map[i]) - 1):
        if map[i][j] == map[i][j + 1] and int(map[i][j]) != 0:
            temp = polygon_center([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                    (len(map[i]) - j, 0, i), (len(map[i]) - j - 1, 0, i)])
            cords[i + 1].append([[(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                             (len(map[i]) - j, 0, i), (len(map[i]) - j - 1, 0, i)],
                             color, dist(temp, cam.pos)])
    return cords