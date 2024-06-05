"""Modul für die Screens, die im Spiel angezeigt werden können."""

import pygame
from geometry_dash_recreation.constants import *

pygame.init()


def return_pause_screen() -> pygame.Surface:
    """
    Liefert ein pygame.Surface mit dem Image für den Pause-Screen.

    :return: pygame.Surface für den Pause-Screen
    """

    return pygame.transform.scale(
        pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/pause_screen.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )


def return_win_screen() -> pygame.Surface:
    """
    Liefert ein pygame.Surface mit dem Image für den Win-Screen.

    :return: pygame.Surface für den Win-Screen
    """

    return pygame.transform.scale(
        pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/win_screen.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )


def return_semi_transparent_screen() -> pygame.Surface:
    """
    Liefert ein pygame.Surface mit einer semitransparenten schwarzen Fläche.

    :return: pygame.Surface mit einer semitransparenten schwarzen Fläche
    """

    return pygame.transform.scale(
        pygame.image.load(f"{ASSETS_FOLDER}/textures/ui/semi_transparent.png").convert_alpha(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
