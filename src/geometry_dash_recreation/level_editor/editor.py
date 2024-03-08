import pygame
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import ui_sprites

pygame.init()
pygame.font.init()

# Sprites
exit_button = ui_sprites.ExitButton()
exit_button.rect.x, exit_button.rect.y = SCREEN_WIDTH * 0.91, SCREEN_HEIGHT * 0.03

ui_other_gr = pygame.sprite.Group(exit_button)

def loop(screen: pygame.Surface) -> tuple:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (EXIT, 0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                return (EXIT, 0)
    
    screen.fill((0, 0, 0))
    ui_other_gr.draw(screen)
    
    return (CONTINUE, 0)
