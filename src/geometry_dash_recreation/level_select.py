import os
import sys

import pygame
from geometry_dash_recreation.constants import *
import geometry_dash_recreation.fonts as fonts
import geometry_dash_recreation.level as level

pygame.init()
pygame.font.init()

# Textanzeigen
levelname_text = fonts.pusab_big.render('', True, (255, 255, 255))
levelname_rect = levelname_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.7))

difficulty_text = fonts.aller_normal.render('', True, (255, 255, 255))
difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

creator_text = fonts.aller_normal.render('', True, (255, 255, 255))
creator_rect = creator_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8))

id_text = fonts.aller_normal.render('', True, (255, 255, 255))
id_rect = id_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.6))

folder_text = fonts.aller_small.render('', True, (255, 255, 255))
folder_rect = folder_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.2))

error_text = fonts.aller_small.render('', True, (255, 0, 0))
error_rect = error_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1))

# Level-Variablen
level_folder = 'levels'
level_list = os.listdir(level_folder)
level_nr = 0

level_folder_edit = False
folder_error = False

level_info = {}


def prev_level() -> None:
    global level_nr
    level_nr -= 1
    if level_nr < 0:
        level_nr += 1


def next_level() -> None:
    global level_nr
    if level_nr == len(level_list) - 1:
        level_nr -= 1
    else:
        level_nr += 1


def select_level() -> str:
    return f'{level_folder}/{level_list[level_nr]}'


def loop(screen: pygame.Surface) -> str:
    global levelname_text, difficulty_text, creator_text, id_text, folder_text, error_text
    global levelname_rect, difficulty_rect, creator_rect, id_rect, folder_rect, error_rect
    global level_folder, level_list, level_nr, level_folder_edit, folder_error, level_info
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if levelname_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                return select_level()
            if folder_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                level_folder_edit = not level_folder_edit
                continue
            if pygame.mouse.get_pos()[0] <= SCREEN_WIDTH / 3:
                prev_level()
            elif pygame.mouse.get_pos()[0] >= SCREEN_WIDTH - SCREEN_WIDTH / 3:
                if pygame.mouse.get_pos()[1] <= SCREEN_HEIGHT / 3:
                    sys.exit(0)
                next_level()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                next_level()
            elif event.key == pygame.K_LEFT:
                prev_level()
            elif event.key == pygame.K_RETURN:
                if level_folder_edit:
                    level_folder_edit = False
                else:
                    return select_level()
            elif event.key == pygame.K_BACKSPACE and level_folder_edit:
                if len(level_folder) > 0:
                    level_folder = level_folder[:-1]
            elif event.key == pygame.K_ESCAPE:
                if not level_folder_edit:
                    sys.exit(0)

            if level_folder_edit and event.key != pygame.K_BACKSPACE and event.key != pygame.K_RETURN:
                level_folder += event.unicode

    screen.fill((50, 0, 25))

    try:
        if not level_folder_edit:
            level_list = os.listdir(level_folder)
            level_info = level.open_level_data(level_folder + "/" + level_list[level_nr])["info"]
        else:
            level_nr = 0
        error_text = fonts.aller_small.render('', True, (255, 0, 0))
        folder_error = False
    except FileNotFoundError:
        error_text = fonts.aller_small.render('Error: Data files not found', True, (255, 0, 0))
        folder_error = True
    except PermissionError:
        error_text = fonts.aller_small.render('Error: Permission denied', True, (255, 0, 0))
        folder_error = True
    except NotADirectoryError:
        error_text = fonts.aller_small.render('Error: Not a directory', True, (255, 0, 0))
        folder_error = True

    if not levelname_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
        levelname_text = fonts.pusab_big.render(f'{level_nr + 1}/{len(level_list)}) {level_info["name"]}', True,
                                                (255, 200, 0), (25, 0, 12))
    else:
        levelname_text = fonts.pusab_big.render(f'{level_nr + 1}/{len(level_list)}) {level_info["name"]}', True,
                                                (0, 255, 0))

    difficulty_text = fonts.aller_normal.render(f'Difficulty: {level_info["difficulty"]}', True,
                                                (255, 255, 255))
    creator_text = fonts.aller_normal.render(f'Created by: {level_info["creator"]}', True, (255, 255, 255))

    if not level_folder_edit:
        folder_text = fonts.aller_small.render(f'Current level folder: {level_folder} (click to edit)', True,
                                               (255, 255, 255))
    else:
        folder_text = fonts.aller_small.render(f'Current level folder: {level_folder}', True,
                                               (0, 255, 0))

    levelname_rect = levelname_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.7))
    difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    creator_rect = creator_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8))
    folder_rect = folder_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.2))
    error_rect = error_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1))

    if not level_folder_edit and not folder_error:
        screen.blit(levelname_text, levelname_rect)
        screen.blit(difficulty_text, difficulty_rect)
        screen.blit(creator_text, creator_rect)
    screen.blit(folder_text, folder_rect)
    screen.blit(error_text, error_rect)

    return ""
