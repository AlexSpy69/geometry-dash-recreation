import pygame
from geometry_dash_recreation.constants import *

pygame.init()


def return_pause_screen() -> pygame.Surface:
    return pygame.transform.scale(
        pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/pause_screen.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )


def return_win_screen() -> pygame.Surface:
    return pygame.transform.scale(
        pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/win_screen.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )


def return_semi_transparent_screen() -> pygame.Surface:
    return pygame.transform.scale(
        pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/semi_transparent.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
