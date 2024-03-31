import sys

import pygame
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import fonts

pygame.init()
pygame.font.init()


def loop(screen: pygame.Surface, error_msg: str) -> int:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return EXIT
    
    error_text = fonts.aller_normal.render(error_msg, True, (255, 255, 255))
    error_rect = error_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    click_text = fonts.aller_normal.render("Click anywhere to continue.", True, (255, 255, 255))
    click_rect = error_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/1.8))
    
    screen.fill((0, 0, 0))
    screen.blit(error_text, error_rect)
    screen.blit(click_text, click_rect)

    return CONTINUE
