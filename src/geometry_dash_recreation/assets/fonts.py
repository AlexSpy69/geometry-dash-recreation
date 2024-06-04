import pygame
from geometry_dash_recreation.constants import *

pygame.init()
pygame.font.init()

# https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame
_circle_cache = {}


def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points


def render(text, font, gfcolor, ocolor, opx):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf


def text_with_outline(text: str, font: pygame.font.Font, outline_size: int=5,
                      normal_color: tuple=(255, 255, 255), outline_color: tuple=(0, 0, 0)) -> pygame.Surface:
    return render(text, font, normal_color, outline_color, outline_size)


pusab_big = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Pusab.otf', int(SCREEN_HEIGHT * 0.08))
pusab_small = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Pusab.otf', int(SCREEN_HEIGHT * 0.05))
pusab_smaller = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Pusab.otf', int(SCREEN_HEIGHT * 0.03))

oxygene_big = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Oxygene 1.ttf', int(SCREEN_HEIGHT * 0.1))

aller_normal = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Aller.ttf', int(SCREEN_HEIGHT * 0.05))
aller_small = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Aller.ttf', int(SCREEN_HEIGHT * 0.03))
aller_smaller = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Aller.ttf', int(SCREEN_HEIGHT * 0.02))
