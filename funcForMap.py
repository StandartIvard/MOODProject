from py3d import polygon_center, dist


def translateMap(name, cam, color):
    f = open('./data/maps/' + name + '.txt')
    mapList = f.readlines()
    cords = list()
    c = 500
    maximum = 0
    for i in range(len(mapList)):
        mapList[i] = ''.join(mapList[i].split())
        temp = mapList[i]
        temp.split()
        temp = map(int, temp)
        maximum = max(max(temp), maximum)

    for i in range(len(mapList) - 1):
        for j in range(len(mapList[i]) - 1):
            if mapList[i][j] == mapList[i][j + 1] == mapList[i + 1][j] == mapList[i + 1][j + 1] and int(mapList[i][j]) != 0:
                temp = polygon_center([((len(mapList[i]) - j - 2) * c, c * int(mapList[i][j]), c * i), ((len(mapList[i]) - j - 1) * c, c * int(mapList[i][j + 1]), c * i),
                                ((len(mapList[i + 1]) - j - 1) * c, c * int(mapList[i + 1][j + 1]), (i + 1) * c),
                                 ((len(mapList[i + 1]) - j - 2) * c, int(mapList[i + 1][j]) * c, (i + 1) * c)])
                cords.append([[(c * (len(mapList[i]) - j - 2), c * int(mapList[i][j]), c * i), (c * (len(mapList[i]) - j - 1), c * int(mapList[i][j + 1]), c * i),
                                (c * (len(mapList[i + 1]) - j - 1), c * int(mapList[i + 1][j + 1]), (i + 1) * c),
                                 (c * (len(mapList[i + 1]) - j - 2), c * int(mapList[i + 1][j]), (i + 1) * c)],
                                 dist(temp, cam.pos), color])

            if mapList[i][j] == mapList[i][j + 1] and mapList[i][j] != '0':
                temp = polygon_center([((len(mapList[i]) - j - 2) * c, c * int(mapList[i][j]), c * i), ((len(mapList[i]) - j - 1) * c, c * int(mapList[i][j + 1]), c * i),
                                 ((len(mapList[i]) - j - 1) * c, 0, c * i), (c * (len(mapList[i]) - j - 2), 0, c * i)])
                cords.append([[((len(mapList[i]) - j - 2) * c, c * int(mapList[i][j]), c * i), ((len(mapList[i]) - j - 1) * c, c * int(mapList[i][j + 1]), c * i),
                                 ((len(mapList[i]) - j - 1) * c, 0, c * i), (c * (len(mapList[i]) - j - 2), 0, c * i)],
                                     dist(temp, cam.pos), color])

            if mapList[i][j] == mapList[i + 1][j] and mapList[i][j] != '0':
                temp = polygon_center([((len(mapList[i]) - j - 1) * c, c * int(mapList[i][j]), c * i), ((len(mapList[i + 1]) - j - 1) * c, c * int(mapList[i + 1][j]), c * (i + 1)),
                               ((len(mapList[i + 1]) - j - 1) * c, 0, c * (i + 1)), ((len(mapList[i]) - j - 1) * c, 0, c * i)])
                cords.append([[((len(mapList[i]) - j - 1) * c, c * int(mapList[i][j]), c * i), ((len(mapList[i + 1]) - j - 1) * c, c * int(mapList[i + 1][j]), c * (i + 1)),
                               ((len(mapList[i + 1]) - j - 1) * c, 0, c * (i + 1)), ((len(mapList[i]) - j - 1) * c, 0, c * i)],
                              dist(temp, cam.pos), color])

            temp = polygon_center([((len(mapList[i]) - j - 2) * c, 0, c * i),
                                   ((len(mapList[i]) - j - 1) * c, 0, c * i),
                                   ((len(mapList[i + 1]) - j - 1) * c, 0, (i + 1) * c),
                                   ((len(mapList[i + 1]) - j - 2) * c, 0, (i + 1) * c)])   # Пол
            cords.append([[(c * (len(mapList[i]) - j - 2), 0, c * i),
                           (c * (len(mapList[i]) - j - 1), 0, c * i),
                           (c * (len(mapList[i + 1]) - j - 1), 0, (i + 1) * c),
                           (c * (len(mapList[i + 1]) - j - 2), 0, (i + 1) * c)],
                          dist(temp, cam.pos), color])

            temp = polygon_center([((len(mapList[i]) - j - 2) * c, maximum, c * i),
                                   ((len(mapList[i]) - j - 1) * c, maximum, c * i),
                                   ((len(mapList[i + 1]) - j - 1) * c, maximum, (i + 1) * c),
                                   ((len(mapList[i + 1]) - j - 2) * c, maximum, (i + 1) * c)])   # Потолок
            cords.append([[(c * (len(mapList[i]) - j - 2), maximum * c, c * i),
                           (c * (len(mapList[i]) - j - 1), maximum * c, c * i),
                           (c * (len(mapList[i + 1]) - j - 1), maximum * c, (i + 1) * c),
                           (c * (len(mapList[i + 1]) - j - 2), maximum * c, (i + 1) * c)],
                          dist(temp, cam.pos), color])

            #if map[i][j] != map[i][j + 1] and map[i][j] != '0' and map[i][j + 1] != '0':
            #    minimal = min(int(map[i][j]), int(map[i][j + 1]))
            #    temp = polygon_center([((len(map[i]) - j - 2) * c, c * minimal, c * i),
            #                           ((len(map[i]) - j - 1) * c, c * minimal, c * i),
            #                           ((len(map[i]) - j - 1) * c, 0, c * i), (c * (len(map[i]) - j - 2), 0, c * i)])
            #    cords.append([[((len(map[i]) - j - 2) * c, c * int(map[i][j]), c * i),
            #                   ((len(map[i]) - j - 1) * c, c * int(map[i][j + 1]), c * i),
            #                   ((len(map[i]) - j - 1) * c, 0, c * i), (c * (len(map[i]) - j - 2), 0, c * i)],
            #                  dist(temp, cam.pos), color])

    i = len(mapList) - 1
    for j in range(len(mapList[i]) - 1):
        if mapList[i][j] == mapList[i][j + 1] and int(mapList[i][j]) != 0:
            temp = polygon_center([((len(mapList[i]) - j - 1) * c, c * int(mapList[i][j]), c * i), ((len(mapList[i]) - j) * c, c * int(mapList[i][j + 1]), c * i),
                    ((len(mapList[i]) - j) * c, 0, c * i), ((len(mapList[i]) - j - 1) * c, 0, c * i)])
            cords.append([[((len(mapList[i]) - j - 1) * c, c * int(mapList[i][j]), c * i), ((len(mapList[i]) - j) * c, c * int(mapList[i][j + 1]), c * i),
                             ((len(mapList[i]) - j) * c, 0, c * i), ((len(mapList[i]) - j - 1) * c, 0, c * i)],
                             dist(temp, cam.pos), color])
    return cords