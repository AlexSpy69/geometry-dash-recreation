from shutil import move
import pygame
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import ui_sprites, game_sprites, fonts
from geometry_dash_recreation.level import level, convert

pygame.init()
pygame.font.init()

# Sprites
exit_button = ui_sprites.ExitButton()
exit_button.rect.x, exit_button.rect.y = SCREEN_WIDTH * 0.91, SCREEN_HEIGHT * 0.03

save_button = ui_sprites.EditorIcon([5, 0, 1, 1])
save_button.rect.x, save_button.rect.y = SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.04

up_button = ui_sprites.EditorIcon([6, 1, 0.45, 0.55])
up_button.rect.left, up_button.rect.top = 0, GROUND_HEIGHT

down_button = ui_sprites.EditorIcon([6.575, 1.5, 0.45, 0.5])
down_button.rect.left, down_button.rect.top = 0, GROUND_HEIGHT+UNIT*1.2

left_button = ui_sprites.EditorIcon([6.5, 1, 0.5, 0.45])
left_button.rect.left, left_button.rect.top = UNIT*1.2, GROUND_HEIGHT

right_button = ui_sprites.EditorIcon([6, 1.575, 0.5, 0.45])
right_button.rect.left, right_button.rect.top = UNIT*1.2, GROUND_HEIGHT+UNIT*1.2

rotate_right_button = ui_sprites.EditorIcon([2, 3, 1, 1])
rotate_right_button.rect.left, rotate_right_button.rect.top = UNIT*2.4, GROUND_HEIGHT

ui_other_gr = pygame.sprite.Group(exit_button, save_button,
                                  up_button, down_button, left_button, right_button,
                                  rotate_right_button)

# Current Object Info
objectinfo_surface = pygame.Surface((800, 400))
objectinfo_surface.fill((0, 0, 0))
objectinfo_surface_rect = pygame.Rect(0, 0, 800, 400)

objecttype_text = fonts.aller_small.render('Type:', True, (255, 255, 255))
objecttype_rect = objecttype_text.get_rect(left=SCREEN_WIDTH * 0.02, top=SCREEN_HEIGHT * 0.05)

objectcolor_text = fonts.aller_small.render('Color:', True, (255, 255, 255))
objectcolor_rect = objecttype_text.get_rect(left=SCREEN_WIDTH * 0.02, top=SCREEN_HEIGHT * 0.10)

movementmode_text = fonts.aller_small.render('Selected:', True, (255, 255, 255))
movementmode_rect = movementmode_text.get_rect(left=SCREEN_WIDTH * 0.02, top=SCREEN_HEIGHT * 0.15)

bg_2_front = False
movement = 0
total_movement = 0
movement_mode = "single"
selected_sprite = game_sprites.HitboxSprite()

def move_rotate_event(sprite, event):
    if event.key == pygame.K_s:
        game_sprites.move_sprite(sprite, 0, UNIT)
    elif event.key == pygame.K_w:
        game_sprites.move_sprite(sprite, 0, -UNIT)
    if event.key == pygame.K_d:
        game_sprites.move_sprite(sprite, UNIT, 0)
    elif event.key == pygame.K_a:
        game_sprites.move_sprite(sprite, -UNIT, 0)
    if event.key == pygame.K_q:
        game_sprites.rotate_sprite(sprite, -45)
    elif event.key == pygame.K_e:
        game_sprites.rotate_sprite(sprite, 45)


def move_rotate_button(sprite):
    if up_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        game_sprites.move_sprite(sprite, 0, -UNIT)
    if down_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        game_sprites.move_sprite(sprite, 0, UNIT)
    if left_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        game_sprites.move_sprite(sprite, UNIT, 0)
    if right_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        game_sprites.move_sprite(sprite, -UNIT, 0)
    if rotate_right_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        game_sprites.rotate_sprite(sprite, -45)


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
            if save_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                return (SAVE_LEVEL, level_gr, total_movement)
            
            if movement_mode == "single":
                move_rotate_button(selected_sprite)
            elif movement_mode == "all":
                for sprite in level_gr:
                    move_rotate_button(sprite)
            
            for sprite in level_gr:
                if sprite.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    selected_sprite = sprite
                    break
            objecttype_text = fonts.aller_small.render(f'Type: {selected_sprite.type}', True, (255, 255, 255))
            objectcolor_text = fonts.aller_small.render(f'Color: {selected_sprite.color}', True, (255, 255, 255))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                movement = 1
            elif event.key == pygame.K_RIGHT:
                movement = -1

            # Position
            if movement_mode == "single":
                move_rotate_event(selected_sprite, event)
            elif movement_mode == "all":
                for sprite in level_gr:
                    move_rotate_event(sprite, event)
            
            # Editor shortcut
            if event.key == pygame.K_m:
                if movement_mode == "single":
                    movement_mode = "all"
                elif movement_mode == "all":
                    movement_mode = "single"
            
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
    
    movementmode_text = fonts.aller_small.render(f'Selected: {movement_mode}', True, (255, 255, 255))

    screen.fill((0, 0, 0))
    bg_gr.draw(screen)
    level_gr.draw(screen)
    ui_other_gr.draw(screen)

    screen.blit(objectinfo_surface, objectinfo_surface_rect)
    screen.blit(objecttype_text, objecttype_rect)
    screen.blit(objectcolor_text, objectcolor_rect)
    screen.blit(movementmode_text, movementmode_rect)
    
    return (CONTINUE, 0)
