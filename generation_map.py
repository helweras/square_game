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


def spawn(card: list, obj: Obj, h, w):
    for y in range(h, h + obj.size[1]):
        for x in range(w, w + obj.size[0]):
            card[y][x] = 1

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
            spawn(pl_map, obj, h, w)
            flag += 1
            w = random.randint(0, 10)
            h = random.randint(0, 8)
        else:
            w = random.randint(0, 10)
            h = random.randint(0, 8)


x = 20  # пиксели в ширину
y = 10  # пиксели в высоту
play_map = [[0 for i in range(x)] for j in range(y)]

control_spawn(3, play_map)
# print(*play_map, sep='\n')
