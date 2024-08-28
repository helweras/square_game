import pygame
import random
import time


class Obj:
    def __init__(self):
        self.size = (10, 2)
        self.coord = ()


class Bonus(Obj):
    def __init__(self):
        super().__init__()
        self.size = (2, 2)


def opt_func(func, *args):
    start = time.perf_counter()
    func(*args)
    stop = time.perf_counter()
    return stop - start


def spawn(card: list, obj: Obj, h, w, mark):
    for y in range(h, h + obj.size[1]):
        for x in range(w, w + obj.size[0]):
            card[y][x] = mark


def spawn_bonus(pl_map, bonus: Bonus):
    pass


def control_spawn(count: int, pl_map: list):
    flag = 0
    w = random.randint(0, 10)
    h = random.randint(0, 8)
    while flag < count:
        if pl_map[h][w] == 0:
            obj = Obj()
            obj.coord = (w, h)
            spawn(pl_map, obj, h, w, 1)
            flag += 1
            w = random.randint(0, 10)
            h = random.randint(0, 8)
        else:
            w = random.randint(0, 10)
            h = random.randint(0, 8)


x = 20  # пиксели в ширину
y = 10  # пиксели в высоту
play_map = [[1 for i in range(x)] for j in range(y)]

for i in range(0, 2):
    for j in range(0, 5):
        play_map[i][j] = 0


# control_spawn(7, play_map)
# print(*play_map, sep='\n')


def check_area(g_map: list, size: tuple, index_x, index_y):
    size_x, size_y = size
    for i in range(index_y, index_y + size_y):
        for j in range(index_x, index_x + size_x):
            if g_map[i][j] != 0:
                return False
    return True


def spawn2(x1, y1, count):
    flag = 0
    w = random.randint(0, y1 - 2)
    h = random.randint(0, x1 - 5)
    while flag != count:
        if check_area(play_map, (5, 2), h, w):
            print(h, w)
            flag += 1
            obj = Obj()
            obj.size = (5, 2)
            obj.coord = (w, h)
            spawn(play_map, obj, w, h, 5)
        else:
            print(h, w)
            w = random.randint(0, y1 - 2)
            h = random.randint(0, x1 - 5)


# print('\n\n\n-----------------------------------------------')
# print(*play_map, sep='\n')
ccc = None
if ccc[0][0]:
    print('xxx')