import pygame
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import ui_sprites, game_sprites, fonts
from geometry_dash_recreation.level import level, convert
from copy import deepcopy

pygame.init()
pygame.font.init()

# Sprites
exit_button = ui_sprites.ExitButton()
exit_button.rect.x, exit_button.rect.y = SCREEN_WIDTH * 0.91, SCREEN_HEIGHT * 0.03

ui_other_gr = pygame.sprite.Group(exit_button)

# Current Object Info
objectinfo_surface = pygame.Surface((800, 400))
objectinfo_surface.fill((0, 0, 0))
objectinfo_surface_rect = pygame.Rect(0, 0, 800, 400)

objecttype_text = fonts.aller_normal.render('Type:', True, (255, 255, 255))
objecttype_rect = objecttype_text.get_rect(center=(SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.05))

objectcolor_text = fonts.aller_normal.render('Color:', True, (255, 255, 255))
objectcolor_rect = objecttype_text.get_rect(center=(SCREEN_WIDTH * 0.05, SCREEN_HEIGHT * 0.11))

movementmode_text = fonts.aller_normal.render('Movement mode:', True, (255, 255, 255))
movementmode_rect = movementmode_text.get_rect(center=(SCREEN_WIDTH * 0.127, SCREEN_HEIGHT * 0.17))

bg_2_front = False
movement = 0
total_movement = 0
movement_mode = "selected"
selected_sprite = game_sprites.HitboxSprite()

def move_event(sprite, event):
    if event.key == pygame.K_s:
        game_sprites.move_sprite(sprite, 0, UNIT)
    elif event.key == pygame.K_w:
        game_sprites.move_sprite(sprite, 0, -UNIT)
    if event.key == pygame.K_d:
        game_sprites.move_sprite(sprite, UNIT, 0)
    elif event.key == pygame.K_a:
        game_sprites.move_sprite(sprite, -UNIT, 0)


def loop(screen: pygame.Surface, level_gr: pygame.sprite.Group, bg_gr: pygame.sprite.Group, 
         background: game_sprites.Background, background_2: game_sprites.Background) -> tuple:
    global bg_2_front, movement, total_movement, movement_mode, selected_sprite
    global objecttype_text, objectcolor_text, movementmode_text
    global objectcolor_text, objectcolor_rect, movementmode_rect
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (EXIT, 0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                return (EXIT, 0)
            for sprite in level_gr:
                if sprite.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    selected_sprite = sprite
                    break
                else:
                    selected_sprite = game_sprites.HitboxSprite()
            objecttype_text = fonts.aller_normal.render(f'Type: {selected_sprite.type}', True, (255, 255, 255))
            objectcolor_text = fonts.aller_normal.render(f'Color: {selected_sprite.color}', True, (255, 255, 255))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement = 1
            elif event.key == pygame.K_RIGHT:
                movement = -1
            # Position
            if movement_mode == "selected":
                move_event(selected_sprite, event)
            elif movement_mode == "all":
                for sprite in level_gr:
                    move_event(sprite, event)
                
            # Rotation
            if event.key == pygame.K_q:
                game_sprites.rotate_sprite(selected_sprite, 45)
            elif event.key == pygame.K_e:
                game_sprites.rotate_sprite(selected_sprite, -45)
            # Editor shortcut
            if event.key == pygame.K_p:
                return (SAVE_LEVEL, level_gr, total_movement)
            elif event.key == pygame.K_m:
                if movement_mode == "selected":
                    movement_mode = "all"
                elif movement_mode == "all":
                    movement_mode = "selected"
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or \
                event.key == pygame.K_RIGHT:
                movement = 0

    background.rect.x += BACKGROUND_SCROLL_SPEED * EDITOR_MOVE_MUL * EDITOR_VIEW_MOVEMENT * movement

    for sprite in level_gr:
        game_sprites.move_sprite(sprite, EDITOR_SPRITE_MOVEMENT * movement, 0)
    total_movement += EDITOR_SPRITE_MOVEMENT * movement
    
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
    
    movementmode_text = fonts.aller_normal.render(f'Movement mode: {movement_mode}', True, (255, 255, 255))

    screen.fill((0, 0, 0))
    bg_gr.draw(screen)
    level_gr.draw(screen)
    ui_other_gr.draw(screen)

    screen.blit(objectinfo_surface, objectinfo_surface_rect)
    screen.blit(objecttype_text, objecttype_rect)
    screen.blit(objectcolor_text, objectcolor_rect)
    screen.blit(movementmode_text, movementmode_rect)
    
    return (CONTINUE, 0)
