from doctest import script_from_examples
import pygame
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import ui_sprites, game_sprites, fonts

pygame.init()
pygame.font.init()

# Sprites
exit_button = ui_sprites.ExitButton()
exit_button.rect.x, exit_button.rect.y = SCREEN_WIDTH * 0.91, SCREEN_HEIGHT * 0.03

ui_other_gr = pygame.sprite.Group(exit_button)

# Current Object Info
objectinfo_surface = pygame.Surface((500, 200))
objectinfo_surface.fill((0, 0, 0))
objectinfo_surface_rect = pygame.Rect(0, 0, 500, 200)

objecttype_text = fonts.aller_normal.render('Type:', True, (255, 255, 255))
objecttype_rect = objecttype_text.get_rect(center=(SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.05))

objectcolor_text = fonts.aller_normal.render('Color:', True, (255, 255, 255))
objectcolor_rect = objecttype_text.get_rect(center=(SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.11))

bg_2_front = False
movement = 0

def loop(screen: pygame.Surface, level_gr: pygame.sprite.Group, bg_gr: pygame.sprite.Group,
         background: game_sprites.Background, background_2: game_sprites.Background) -> tuple:
    global bg_2_front, movement
    global objecttype_text, objectcolor_text
    global objectcolor_text, objectcolor_rect
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (EXIT, 0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                return (EXIT, 0)
            for sprite in level_gr:
                if sprite.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    objecttype_text = fonts.aller_normal.render(f'Type: {sprite.type}', True, (255, 255, 255))
                    objectcolor_text = fonts.aller_normal.render(f'Color: {sprite.color}', True, (255, 255, 255))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement = 1
            elif event.key == pygame.K_RIGHT:
                movement = -1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or \
                event.key == pygame.K_RIGHT:
                movement = 0

    background.rect.x += BACKGROUND_SCROLL_SPEED * EDITOR_MOVE_MUL * EDITOR_VIEW_MOVEMENT * movement

    for sprite in level_gr:
        sprite.rect.x += LEVEL_SCROLL_SPEED * EDITOR_MOVE_MUL * EDITOR_VIEW_MOVEMENT * movement
        sprite.hitbox.center = sprite.rect.center
    
    if background.rect.right == 0:
        background.rect.left = background_2.rect.width
        bg_2_front = True
    elif background_2.rect.right == 0:
        background.rect.left = 0
        bg_2_front = False
    
    if not bg_2_front:
        background_2.rect.left = background.rect.right
    else:
        background_2.rect.right = background.rect.left

    screen.fill((0, 0, 0))
    bg_gr.draw(screen)
    level_gr.draw(screen)
    ui_other_gr.draw(screen)

    screen.blit(objectinfo_surface, objectinfo_surface_rect)
    screen.blit(objecttype_text, objecttype_rect)
    screen.blit(objectcolor_text, objectcolor_rect)
    
    return (CONTINUE, 0)
