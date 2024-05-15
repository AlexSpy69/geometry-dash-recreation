import pygame
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import ui_sprites, game_sprites, fonts
from geometry_dash_recreation import util

pygame.init()
pygame.font.init()

# Sprites
exit_button = ui_sprites.ExitButton()
exit_button.rect.x, exit_button.rect.y = SCREEN_WIDTH * 0.91, SCREEN_HEIGHT * 0.03

save_button = ui_sprites.EditorIcon([5, 0, 1, 1])
save_button.rect.x, save_button.rect.y = SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.04

up_button = ui_sprites.EditorIcon([6, 1, 0.45, 0.55])
up_button.rect.left, up_button.rect.top = UNIT*3.5, GROUND_HEIGHT

down_button = ui_sprites.EditorIcon([6.575, 1.5, 0.45, 0.5])
down_button.rect.left, down_button.rect.top = UNIT*3.5, GROUND_HEIGHT+UNIT*1.2

left_button = ui_sprites.EditorIcon([6.5, 1, 0.5, 0.45])
left_button.rect.left, left_button.rect.top = UNIT*3.5+UNIT*1.2, GROUND_HEIGHT

right_button = ui_sprites.EditorIcon([6, 1.575, 0.5, 0.45])
right_button.rect.left, right_button.rect.top = UNIT*3.5+UNIT*1.2, GROUND_HEIGHT+UNIT*1.2

rotate_right_button = ui_sprites.EditorIcon([2, 3, 1, 1])
rotate_right_button.rect.left, rotate_right_button.rect.top = UNIT*3.5+UNIT*2.4, GROUND_HEIGHT

delete_button = ui_sprites.EditorIcon([4, 0, 1, 1])
delete_button.rect.left, delete_button.rect.top = UNIT*3.5+UNIT*2.4, GROUND_HEIGHT+UNIT*1.2

option_up = ui_sprites.EditorIcon([6, 1, 0.45, 0.55])
option_up.rect.left, option_up.rect.top = UNIT*13, GROUND_HEIGHT

option_down = ui_sprites.EditorIcon([6.575, 1.5, 0.45, 0.5])
option_down.rect.left, option_down.rect.top = UNIT*13, GROUND_HEIGHT+UNIT*1.2

option_left = ui_sprites.EditorIcon([6.5, 1, 0.5, 0.45])
option_left.rect.left, option_left.rect.top = UNIT*13+UNIT*1.2, GROUND_HEIGHT

option_right = ui_sprites.EditorIcon([6, 1.575, 0.5, 0.45])
option_right.rect.left, option_right.rect.top = UNIT*13+UNIT*1.2, GROUND_HEIGHT+UNIT*1.2

level_move_left = ui_sprites.Arrow(False)
level_move_left.rect.x, level_move_left.rect.y = SCREEN_WIDTH * 0.04, SCREEN_HEIGHT * 0.45

level_move_right = ui_sprites.Arrow(True)
level_move_right.rect.x, level_move_right.rect.y = SCREEN_WIDTH * 0.90, SCREEN_HEIGHT * 0.45

editor_bar_label = ui_sprites.EditorBarLabel()
editor_bar_label.rect.left, editor_bar_label.rect.top = 0, GROUND_HEIGHT

ui_other_gr = pygame.sprite.Group(exit_button, save_button,
                                  up_button, down_button, left_button, right_button,
                                  rotate_right_button, delete_button, 
                                  option_up, option_down, option_left,
                                  option_right, editor_bar_label,
                                  level_move_left, level_move_right)

# Current Object Info
objectinfo_surface = pygame.Surface((SCREEN_WIDTH * 0.23, SCREEN_HEIGHT * 0.37))
objectinfo_surface.fill((0, 0, 0))
objectinfo_surface_rect = pygame.Rect(0, 0, SCREEN_WIDTH * 0.23, SCREEN_HEIGHT * 0.37)

imgfile_text = fonts.aller_small.render('Image Name:', True, (255, 255, 255))
imgfile_rect = imgfile_text.get_rect(left=SCREEN_WIDTH * 0.02, top=SCREEN_HEIGHT * 0.05)

objecttype_text = fonts.aller_small.render('Type:', True, (255, 255, 255))
objecttype_rect = objecttype_text.get_rect(left=SCREEN_WIDTH * 0.02, top=SCREEN_HEIGHT * 0.10)

objectcolor_text = fonts.aller_small.render('Color:', True, (255, 255, 255))
objectcolor_rect = objecttype_text.get_rect(left=SCREEN_WIDTH * 0.02, top=SCREEN_HEIGHT * 0.15)

movementmode_text = fonts.aller_small.render('Selected:', True, (255, 255, 255))
movementmode_rect = movementmode_text.get_rect(left=SCREEN_WIDTH * 0.02, top=SCREEN_HEIGHT * 0.25)

bg_2_front = False
movement = 0
total_movement = 0
movement_mode = "single"
selected_sprite = game_sprites.HitboxSprite()

option = 0
img_index = 0
type_index = 0
color_index = 0


def snap_position(xpos: int, ypos: int, add_unit=0) -> tuple:
    ypos -= 1
    xpos += 1
    return (round(xpos - xpos % UNIT + total_movement % UNIT, 2),
            round(ypos - ypos % UNIT + UNIT * int(add_unit) + UNIT, 2))


def current_to_initial_x(x: int):
    global total_movement
    return x - total_movement


def add_component(level_gr: pygame.sprite.Group, component: game_sprites.Component) -> game_sprites.Component:
    component.set_sprite_position(snap_position(*util.iter_add(pygame.mouse.get_pos(), (0, 0))), "lb")
    component.initial_rect.x = current_to_initial_x(component.rect.x)
    component.initial_rect.y = component.rect.y
    level_gr.add(component)
    return component


def move_rotate_event(sprite: game_sprites.HitboxSprite, event):
    global selected_sprite
    rotate = False

    if event.key == pygame.K_s:
        sprite.move_initial(0, UNIT)
    elif event.key == pygame.K_w:
        sprite.move_initial(0, -UNIT)
    if event.key == pygame.K_d:
        sprite.move_initial(UNIT, 0)
    elif event.key == pygame.K_a:
        sprite.move_initial(-UNIT, 0)
    elif event.key == pygame.K_q or event.key == pygame.K_e:
        angle = 45 if event.key == pygame.K_q else -45
        sprite.rotate_sprite(angle)
        rotate = True
    elif event.key == pygame.K_DELETE:
        sprite.kill()
        selected_sprite = game_sprites.HitboxSprite()
    else:
        return
    
    if not rotate:
        sprite.set_sprite_position(snap_position(sprite.rect.left, sprite.rect.bottom), "lb")


def move_rotate_button(sprite: game_sprites.HitboxSprite) -> bool:
    global selected_sprite
    rotate = False

    if up_button.rect.collidepoint(*pygame.mouse.get_pos()):
        sprite.move_initial(0, -UNIT)
    elif down_button.rect.collidepoint(*pygame.mouse.get_pos()):
        sprite.move_initial(0, UNIT)
    elif left_button.rect.collidepoint(*pygame.mouse.get_pos()):
        sprite.move_initial(UNIT, 0)
    elif right_button.rect.collidepoint(*pygame.mouse.get_pos()):
        sprite.move_initial(-UNIT, 0)
    elif rotate_right_button.rect.collidepoint(*pygame.mouse.get_pos()):
        sprite.rotate_sprite(-45)
        rotate = True
    elif delete_button.rect.collidepoint(*pygame.mouse.get_pos()):
        sprite.kill()
        selected_sprite = game_sprites.HitboxSprite()
    else:
        return False
    
    if not rotate:
        sprite.set_sprite_position(snap_position(sprite.rect.left, sprite.rect.bottom), "lb")

    return True


def update_label():
    global imgfile_text, objecttype_text, objectcolor_text, movementmode_text, option
    imgfile_text = fonts.aller_small.render(
        f'Image Name: {selected_sprite.image_filename[len(ASSETS_FOLDER + "/textures/components")::]}',
        True, (0, 255, 0) if option == 1 else (255, 255, 255)
    )
    objecttype_text = fonts.aller_small.render(f'Type: {selected_sprite.type if selected_sprite.type != "" else "(no value)"}',
                                               True, (0, 255, 0) if option == 2 else (255, 255, 255))
    objectcolor_text = fonts.aller_small.render(f'Color: {selected_sprite.color if selected_sprite.color != "" else "(no value)"}',
                                                True, (0, 255, 0) if option == 3 else (255, 255, 255))
    movementmode_text = fonts.aller_small.render(f'Selected: {movement_mode}', True, (255, 255, 255))


def option_handle(option, option_increase):
    global selected_sprite, img_index, type_index, color_index
    if option == 1 and type(selected_sprite) != game_sprites.HitboxSprite:
        img_index += option_increase
        img_index %= len(COMPONENT_IMGFILE_LIST)
        temp_initial_rect = selected_sprite.initial_rect.left, selected_sprite.initial_rect.bottom
        temp_rect = selected_sprite.rect.left, selected_sprite.rect.bottom
        selected_sprite.image_filename = COMPONENT_IMGFILE_LIST[img_index]
        selected_sprite.size, selected_sprite.angle, selected_sprite.hb_mul, selected_sprite.type, selected_sprite.color = \
            util.csv_reader(selected_sprite.image_filename + ".csv")
        selected_sprite.real_init()
        selected_sprite.initial_rect.left, selected_sprite.initial_rect.bottom = temp_initial_rect
        selected_sprite.rect.left, selected_sprite.rect.bottom = temp_rect
        selected_sprite.set_sprite_position(snap_position(selected_sprite.rect.left, selected_sprite.rect.bottom), "lb")
        
    elif option == 2:
        type_index += option_increase
        type_index %= len(COMPONENT_TYPE_LIST)
        selected_sprite.type = COMPONENT_TYPE_LIST[type_index]
    
    elif option == 3:
        color_index += option_increase
        color_index %= len(COMPONENT_COLOR_LIST)
        selected_sprite.color = COMPONENT_COLOR_LIST[color_index]


def option_button() -> bool:
    global option
    if option_up.rect.collidepoint(*pygame.mouse.get_pos()):
        option -= 1
    elif option_down.rect.collidepoint(*pygame.mouse.get_pos()):
        option += 1
    elif option_left.rect.collidepoint(*pygame.mouse.get_pos()):
        option_handle(option, -1)
    elif option_right.rect.collidepoint(*pygame.mouse.get_pos()):
        option_handle(option, 1)
    else:
        return False
    
    option = util.limit(option, 3, True)

    return True


def move_level_button() -> bool:
    global movement
    if level_move_left.rect.collidepoint(*pygame.mouse.get_pos()):
        movement = 1
    elif level_move_right.rect.collidepoint(*pygame.mouse.get_pos()):
        movement = -1
    else:
        return False
    return True


def draw_grid(screen):
    global total_movement
    for x in range(0, int(SCREEN_WIDTH / UNIT)):
        pygame.draw.line(screen, (0, 0, 0), snap_position(x * UNIT, -UNIT), (snap_position(x * UNIT, 0)[0], SCREEN_HEIGHT))
    for y in range(0, int(SCREEN_HEIGHT / UNIT)):
        pygame.draw.line(screen, (0, 0, 0), (0, y * UNIT), (SCREEN_WIDTH, y * UNIT))


def loop(screen: pygame.Surface, level_gr: pygame.sprite.Group, bg_gr: pygame.sprite.Group, 
         background: game_sprites.Background, background_2: game_sprites.Background) -> tuple:
    global bg_2_front, movement, total_movement, movement_mode, selected_sprite, option, type_index, color_index, img_index
    global objecttype_text, objectcolor_text, movementmode_text, imgfile_text
    global objectcolor_text, objectcolor_rect, movementmode_rect, imgfile_rect, objectinfo_surface_rect
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (EXIT, None, None)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.rect.collidepoint(*pygame.mouse.get_pos()):
                total_movement = 0
                return (EXIT, None, None)
            elif save_button.rect.collidepoint(*pygame.mouse.get_pos()):
                return (SAVE_LEVEL, level_gr, total_movement)            
            elif objectinfo_surface_rect.collidepoint(*pygame.mouse.get_pos()):
                option += 1
                option = util.limit(option, 3, True)
                update_label()
                break

            if option_button():
                update_label()
                break
            
            if move_level_button():
                break
            
            if movement_mode == "single":
                if move_rotate_button(selected_sprite):
                    break
            elif movement_mode == "all":
                for sprite in level_gr:
                    if move_rotate_button(sprite):
                        break
            
            for sprite in level_gr:
                if sprite.rect.collidepoint(*pygame.mouse.get_pos()):
                    selected_sprite = sprite
                    break
            
            if not "sprite" in locals():
                sprite = game_sprites.HitboxSprite()

            if selected_sprite is not sprite:
                selected_sprite = add_component(level_gr, game_sprites.Component(
                    imgfile=f"{ASSETS_FOLDER}/textures/components/blocks/RegularBlock01.png",
                    pos=(0, 0),
                    size=(1, 1),
                    hb_mul=1,
                    type_="platform",
                    color=""
                ))
            
            update_label()

        elif event.type == pygame.MOUSEBUTTONUP:
            if level_move_left.rect.collidepoint(*pygame.mouse.get_pos()) or \
                level_move_right.rect.collidepoint(*pygame.mouse.get_pos()):
                movement = 0
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selected_sprite = game_sprites.HitboxSprite()

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
            
            if event.key == pygame.K_UP:
                option -= 1
            elif event.key == pygame.K_DOWN:
                option += 1
            option = util.limit(option, 3, True)

            if event.key == pygame.K_o:
                option_handle(option, 1)
            elif event.key == pygame.K_l:
                option_handle(option, -1)
            
            update_label()
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or \
                event.key == pygame.K_RIGHT:
                movement = 0
    
    if background.rect.left >= 0 and movement == 1:
        for sprite in level_gr:
            sprite.move_sprite(-total_movement, 0)
        total_movement = 0
        movement = 0
    
    type_index, color_index = COMPONENT_TYPE_LIST.index(selected_sprite.type), COMPONENT_COLOR_LIST.index(selected_sprite.color)

    background.rect.x += BACKGROUND_SCROLL_SPEED * EDITOR_MOVE_MUL * EDITOR_VIEW_MOVEMENT * movement

    total_movement += EDITOR_SPRITE_MOVEMENT * movement
    for sprite in level_gr:
        sprite.set_sprite_position((sprite.initial_rect.x + total_movement, sprite.initial_rect.y))

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

    draw_grid(screen)
    ui_other_gr.draw(screen)

    # screen.blit(objectinfo_surface, objectinfo_surface_rect)
    screen.blit(imgfile_text, imgfile_rect)
    screen.blit(objecttype_text, objecttype_rect)
    screen.blit(objectcolor_text, objectcolor_rect)
    screen.blit(movementmode_text, movementmode_rect)
    
    return (CONTINUE, None, None)
