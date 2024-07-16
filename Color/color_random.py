import tkinter as tk
from random import choice


def get_colors():
    with open(r'C:\Users\paa18\PycharmProjects\game\Color\colors.txt', 'r', encoding='utf-8') as file:  # список цветов
        colors_key = []
        colors_item = []
        for color in file:
            tmp = ''
            for i in color.split():
                if '#' not in i:
                    tmp += i + ' '
                else:
                    colors_key.append(i)
                    colors_item.append(tmp.rstrip())
                    break
    colors_dict = dict(zip(colors_key, colors_item))
    return colors_dict


def change_color():
    pass
