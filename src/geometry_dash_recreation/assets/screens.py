import pygame
from geometry_dash_recreation.constants import *

pygame.init()

def returnPauseScreen() -> pygame.Surface:
    return pygame.transform.scale(
        pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/pause_screen.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

def returnWinScreen() -> pygame.Surface:
    return pygame.transform.scale(
        pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/win_screen.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
