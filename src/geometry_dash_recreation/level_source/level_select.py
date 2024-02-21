import os
import sys

import pygame
from geometry_dash_recreation.constants import *
import geometry_dash_recreation.assets_source.fonts as fonts
import geometry_dash_recreation.level_source.level as level
import geometry_dash_recreation.save_file_source.save_file as save_file

pygame.init()
pygame.font.init()

# Textanzeigen
levelname_text = fonts.pusab_big.render('', True, (255, 255, 255))
levelname_rect = levelname_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.7))

difficulty_text = fonts.aller_normal.render('', True, (255, 255, 255))
difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

creator_text = fonts.aller_normal.render('', True, (255, 255, 255))
creator_rect = creator_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8))

comp_text = fonts.aller_normal.render('', True, (255, 255, 255))
comp_rect = comp_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.6))

folder_text = fonts.aller_small.render('', True, (255, 255, 255))
folder_rect = folder_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.2))

error_text = fonts.aller_small.render('', True, (255, 0, 0))
error_rect = error_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1))

playerdata_text = fonts.pusab_small.render("View Player Data", True, (255, 255, 255))
playerdata_rect = playerdata_text.get_rect(center=(SCREEN_WIDTH * 0.15, SCREEN_HEIGHT * 0.05))

# Level-Variablen
level_folder = LEVELS_FOLDER
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


def selected_level() -> str:
    return f'{level_folder}/{level_list[level_nr]}'


def current_level_percentage() -> int:
    return save_file.open_sf(SAVE_FILE_PATH).get_level_percent(selected_level())


def loop(screen: pygame.Surface) -> str:
    global levelname_text, difficulty_text, creator_text, comp_text, folder_text, error_text, playerdata_text
    global levelname_rect, difficulty_rect, creator_rect, comp_rect, folder_rect, error_rect, playerdata_rect
    global level_folder, level_list, level_nr, level_folder_edit, folder_error, level_info
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if levelname_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                return selected_level()
            if folder_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                level_folder_edit = not level_folder_edit
                continue
            if pygame.mouse.get_pos()[0] <= SCREEN_WIDTH / 3:
                if pygame.mouse.get_pos()[1] <= SCREEN_HEIGHT / 3:
                    return VIEW_SAVE_FILE
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
                    return selected_level()
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

    difficulty_text = fonts.aller_normal.render(f'Difficulty: {DIFFICULTY[int(level_info["stars"])]}, '
                                                f'{level_info["stars"]}*', True, (255, 255, 255))
    creator_text = fonts.aller_normal.render(f'Created by: {level_info["creator"]}', True, (255, 255, 255))
    if current_level_percentage() == 100:
        comp_text = fonts.aller_normal.render(f'{current_level_percentage()}% Completed', True, (100, 255, 100))
    else:
        comp_text = fonts.aller_normal.render(f'{current_level_percentage()}% Completed', True, (255, 100, 100))

    if not level_folder_edit:
        if level_folder == LEVELS_FOLDER:
            folder_text = fonts.aller_small.render(f'Current level folder: Default level folder', True, (255, 255, 255))
        else:
            folder_text = fonts.aller_small.render(f'Current level folder: {level_folder}', True, (255, 255, 255))
    else:
        folder_text = fonts.aller_small.render(f'Current level folder: {level_folder}', True,
                                               (0, 255, 0))

    levelname_rect = levelname_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2.7))
    difficulty_rect = difficulty_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    creator_rect = creator_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.8))
    comp_rect = comp_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.6))
    folder_rect = folder_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.2))
    error_rect = error_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.1))

    if not level_folder_edit and not folder_error:
        screen.blit(levelname_text, levelname_rect)
        screen.blit(difficulty_text, difficulty_rect)
        screen.blit(creator_text, creator_rect)
        screen.blit(comp_text, comp_rect)
    screen.blit(folder_text, folder_rect)
    screen.blit(error_text, error_rect)
    screen.blit(playerdata_text, playerdata_rect)

    return ""
