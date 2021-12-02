def translateMap(name):
    f = open('./maps/' + name + '.txt')
    map = f.readlines()
    cords = list()
    for i in range(len(map)):
        map[i] = ''.join(map[i].split())
        cords.append([])
        for j in range(len(map[i])):
            cords[i].append((int(map[i][j]), i, (len(map[i]) - j) - 1))
    return cords

a = translateMap('mapName')
for i in a:
    print(i)