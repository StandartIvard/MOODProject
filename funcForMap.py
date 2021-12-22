def translateMap(name):
    f = open('./data/maps/' + name + '.txt')
    map = f.readlines()
    cords = list()
                                            #  (int(map[i][j]), i, (len(map[i]) - j) - 1)
    for i in range(len(map) - 1):
        cords.append([])
        map[i] = ''.join(map[i].split())
        map[i + 1] = ''.join(map[i + 1].split())
        for j in range(len(map[i]) - 1):
            if map[i][j] == map[i][j + 1] == map[i + 1][j] == map[i + 1][j + 1]:
                cords[i].append([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                                (len(map[i + 1]) - j, int(map[i + 1][j]), i + 1),
                                 (len(map[i + 1]) - j - 1, int(map[i + 1][j]), i + 1)])
            elif map[i][j] != map[i + 1][j + 1]:
                if map[i][j] == map[i][j + 1]:
                    cords[i].append([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i]) - j, int(map[i][j + 1]), i),
                                     (len(map[i]) - j, 0, i), (len(map[i]) - j - 1, 0, i)])
                if map[i][j] == map[i + 1][j]:
                    cords[i].append([(len(map[i]) - j - 1, int(map[i][j]), i), (len(map[i + 1]) - j, int(map[i][j]), i),
                                     (len(map[i + 1]) - j, 0, i), (len(map[i]) - j - 1, 0, i)])
    return cords


a = translateMap('mapName')
for i in a:
    print(i)