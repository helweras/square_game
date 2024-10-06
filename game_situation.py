# import pygame
# from character import MainPlayer
# import obj
# import sys
# import pygame


def left(obj_for_collision, obst):
    return (obst.rect.right - obj_for_collision.rect.left) < (obj_for_collision.rect.bottom - obst.rect.top)


def right(obj_for_collision, obst):
    return obj_for_collision.rect.right - obst.rect.left < obj_for_collision.rect.bottom - obst.rect.top


def underarm_left(obj_for_collision, obst):
    return obst.rect.right - obj_for_collision.rect.left > obst.rect.bottom - obj_for_collision.rect.top


def underarm_right(obj_for_collision, obst):
    return obj_for_collision.rect.right - obst.rect.left > obst.rect.bottom - obj_for_collision.rect.top


def collision(obj_for_collision, obst):
    if obj_for_collision.rect.colliderect(obst):
        x, y = obj_for_collision.get_direction()
        # Коллизии с препятствием при прямом столкновении

        if x > 0 and y == 0:  # справа
            obj_for_collision.rect.right = obst.rect.left
        elif x < 0 and y == 0:  # слева
            obj_for_collision.rect.left = obst.rect.right
        elif y < 0 and x == 0:  # снизу
            obj_for_collision.rect.top = obst.rect.bottom
        elif y > 0 and x == 0:  # сверху
            obj_for_collision.rect.bottom = obst.rect.top

        # Коллизии с препятствием при диагональном соприкосновении

        elif (x < 0 and (y < 0 or y > 0)) and left(obj_for_collision, obst) and not underarm_left(obj_for_collision, obst):  # слева + верх и низ
            obj_for_collision.rect.left = obst.rect.right

        elif (x > 0 and (y < 0 or y > 0)) and right(obj_for_collision, obst) and not underarm_right(obj_for_collision,
                                                                                       obst):  # справа + верх и низ
            obj_for_collision.rect.right = obst.rect.left

        elif (y < 0 and (x < 0 or x > 0)) and obj_for_collision.rect.bottom > obst.rect.bottom:
            obj_for_collision.rect.top = obst.rect.bottom

        elif (y > 0 and (x < 0 or x > 0)) and obj_for_collision.rect.top < obst.rect.top:
            obj_for_collision.rect.bottom = obst.rect.top
        return True


def collision_mask(obj_for_collision, obst, obst_mask):
    offset = (obst.rect.x - obj_for_collision.rect.x, obst.rect.y - obj_for_collision.rect.y)
    collision_point = obj_for_collision.mask.overlap(obst_mask, offset)
    if collision_point:
        print('xxx')
