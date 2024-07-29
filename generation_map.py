import pygame
import random
import time


class Obj:
    def __init__(self):
        self.size = (150, 20)
        self.coord = ()


def opt_func(func, *args):
    start = time.perf_counter()
    func(*args)
    stop = time.perf_counter()
    return stop - start


def spawn(card: list, obj: Obj, h, w):
    for y in range(h, h + obj.size[1]):
        for x in range(w, w + obj.size[0]):
            card[y][x] = 1


v = []


def control_spawn(count: int, pl_map: list):
    flag = 0
    w = random.randint(50, 950)
    h = random.randint(50, 1050)
    while flag < count:
        if pl_map[w][h] == 0:
            obj = Obj()
            obj.coord = (h, w)
            v.append(obj)
            spawn(pl_map, obj, w, h)
            flag += 1
            w = random.randint(50, 950)
            h = random.randint(50, 1050)
        else:
            w = random.randint(50, 950)
            h = random.randint(50, 1050)


x = 1250  # пиксели в ширину
y = 1000  # пиксели в высоту
play_map = [[0 for i in range(x)] for j in range(y)]

