import pygame
from geometry_dash_recreation.constants import *

pygame.init()
pygame.font.init()

pusab_big = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Pusab.otf', int(SCREEN_HEIGHT * 0.08))
pusab_small = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Pusab.otf', int(SCREEN_HEIGHT * 0.05))
pusab_smaller = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Pusab.otf', int(SCREEN_HEIGHT * 0.03))

oxygene_big = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Oxygene 1.ttf', int(SCREEN_HEIGHT * 0.1))

aller_normal = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Aller.ttf', int(SCREEN_HEIGHT * 0.05))
aller_small = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Aller.ttf', int(SCREEN_HEIGHT * 0.03))
aller_smaller = pygame.font.Font(f'{ASSETS_FOLDER}/fonts/Aller.ttf', int(SCREEN_HEIGHT * 0.02))
