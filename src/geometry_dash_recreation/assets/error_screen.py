"""Modul, das den Error-Screen des Spiels enthält."""

import sys
import pygame
from geometry_dash_recreation import constants as const
from geometry_dash_recreation.assets import fonts

pygame.init()
pygame.font.init()


def loop(screen: pygame.Surface, error_msg: str) -> int:
    """
    Loop-Funktion des Error-Screens, die in gdr.base und gdr.level.level_select aufgerufen wird.

    :param screen: Der pygame.Surface, auf den der Screen gezeichnet werden soll
    :param error_msg: Die Fehlermeldung, die angezeigt werden soll.
    :return:
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN or \
                event.type == pygame.KEYDOWN:
            return const.EXIT

    error_text = fonts.aller_normal.render(error_msg, True, (255, 255, 255))
    error_rect = error_text.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2))

    click_text = fonts.aller_normal.render("Click anywhere to continue.", True, (255, 255, 255))
    click_rect = error_text.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 1.8))

    screen.fill((0, 0, 0))
    screen.blit(error_text, error_rect)
    screen.blit(click_text, click_rect)

    return const.CONTINUE
