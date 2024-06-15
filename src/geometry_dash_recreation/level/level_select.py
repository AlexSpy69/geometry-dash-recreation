"""Modul, das für das Levelmenü zuständig ist"""

import os
import sys

import pygame
from geometry_dash_recreation import constants as const
from geometry_dash_recreation.assets import fonts, ui_sprites, error_screen
from geometry_dash_recreation.level import convert, level_files
from geometry_dash_recreation.save_file import save_file

pygame.init()
pygame.font.init()

try:
    os.mkdir(const.USER_LEVELS_FOLDER)
except FileExistsError:
    pass

# Textanzeigen
levelname_text = fonts.pusab_big.render('', True, (255, 255, 255))
levelname_rect = levelname_text.get_rect()

difficulty_text = fonts.aller_normal.render('', True, (255, 255, 255))
difficulty_rect = difficulty_text.get_rect()

creator_text = fonts.aller_normal.render('', True, (255, 255, 255))
creator_rect = creator_text.get_rect()

comp_text = fonts.aller_normal.render('', True, (255, 255, 255))
comp_rect = comp_text.get_rect()

folder_text = fonts.aller_small.render('', True, (255, 255, 255))
folder_rect = folder_text.get_rect()

error_text = fonts.aller_small.render('', True, (255, 0, 0))
error_rect = error_text.get_rect()

# Sprites
arrow_left = ui_sprites.Arrow(right=False)
arrow_left.rect.x, arrow_left.rect.y = const.SCREEN_WIDTH * 0.04, const.SCREEN_HEIGHT * 0.45
arrow_right = ui_sprites.Arrow(right=True)
arrow_right.rect.x, arrow_right.rect.y = const.SCREEN_WIDTH * 0.90, const.SCREEN_HEIGHT * 0.45
arrow_gr = pygame.sprite.Group(arrow_left, arrow_right)

user_icon = ui_sprites.UserIcon()
user_icon.rect.x, user_icon.rect.y = const.SCREEN_WIDTH * 0.02, const.SCREEN_HEIGHT * 0.015

build_icon = ui_sprites.BuildIcon()
build_icon.rect.x, build_icon.rect.y = const.SCREEN_WIDTH * 0.68, const.SCREEN_HEIGHT * 0.04

plus_icon = ui_sprites.PlusIcon()
plus_icon.rect.x, plus_icon.rect.y = const.SCREEN_WIDTH * 0.74, const.SCREEN_HEIGHT * 0.04

trash_icon = ui_sprites.TrashIcon()
trash_icon.rect.x, trash_icon.rect.y = const.SCREEN_WIDTH * 0.8, const.SCREEN_HEIGHT * 0.04

exit_button = ui_sprites.ExitButton()
exit_button.rect.x, exit_button.rect.y = const.SCREEN_WIDTH * 0.91, const.SCREEN_HEIGHT * 0.03

ui_other_gr = pygame.sprite.Group(user_icon, build_icon, exit_button, plus_icon, trash_icon)

# Level-Variablen
level_folder = const.MAIN_LEVELS_FOLDER
level_list = os.listdir(level_folder)
level_nr = 0

level_folder_edit = False
folder_error = False

level_info = {}


def prev_level() -> None:
    """
    Wählt das Level in der Level-Liste aus, das sich vor dem aktuellen Level befindet.

    :return:
    """

    global level_nr
    if len(level_list) in (0, 1):
        return
    level_nr -= 1
    level_nr %= len(level_list)


def next_level() -> None:
    """
    Wählt das Level in der Level-Liste aus, das sich nach dem aktuellen Level befindet.

    :return:
    """

    global level_nr
    if len(level_list) in (0, 1):
        return
    level_nr += 1
    level_nr %= len(level_list)


def selected_level() -> str:
    """
    Liefert den Dateinamen des Levels, das gerade ausgewählt ist.

    :return: Dateiname des ausgewählten Levels
    """

    if len(level_list) != 0:
        return f'{level_folder}/{level_list[level_nr]}'
    else:
        return ""


def current_level_percentage() -> int:
    """
    Liefert den maximalen Prozentsatz, den der Spieler im aktuellen Level erreicht hat

    :return: Der Prozentsatz
    """

    return save_file.open_sf(const.SAVE_FILE_PATH).get_level_percent(selected_level())


def sort_level_list_by_difficulty() -> None:
    """
    Sortiert die Level-Liste (globale Variable level_list) anhand der Schwierigkeitsgrade der Levels.

    :return:
    """

    def get_level_stars(levelname: str) -> int:
        return int(level_files.open_level_data(f'{level_folder}/{levelname}')["info"]["stars"])

    for i in range(len(level_list)):
        for j in range(i, len(level_list)):
            if get_level_stars(level_list[i]) > get_level_stars(level_list[j]):
                level_list[i], level_list[j] = level_list[j], level_list[i]


def loop_no_exception(screen: pygame.Surface) -> tuple:
    """
    Loop-Funktion für das Levelmenü. Fehler, die während dem Laufen der Funktion auftreten, können nicht abgefangen
    werden.

    :param screen: pygame.Surface, auf das das Levelmenü gezeichnet werden soll.
    :return: Tupel mit einem Exit-Code als erstes Element und dem Levelnamen als zweites
        (Ausnahmen: (VIEW_SAVE_FILE, None); (NEW_LEVEL, level_folder))
    """

    global levelname_text, difficulty_text, creator_text, comp_text, folder_text, error_text
    global levelname_rect, difficulty_rect, creator_rect, comp_rect, folder_rect, error_rect
    global level_folder, level_list, level_nr, level_folder_edit, folder_error, level_info
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if levelname_rect.collidepoint(*pygame.mouse.get_pos()):
                if len(level_list) != 0:
                    return const.PLAY_LEVEL, selected_level()
            elif folder_rect.collidepoint(*pygame.mouse.get_pos()):
                if not level_folder_edit:
                    level_folder_edit = True
                else:
                    level_folder = level_folder.replace("Main levels folder", const.MAIN_LEVELS_FOLDER)
                    level_folder = level_folder.replace("User levels folder", const.USER_LEVELS_FOLDER)
                    level_folder_edit = False
                continue
            elif user_icon.rect.collidepoint(*pygame.mouse.get_pos()):
                return const.VIEW_SAVE_FILE, None
            elif build_icon.rect.collidepoint(*pygame.mouse.get_pos()):
                return const.OPEN_LEVEL_EDITOR, selected_level()
            elif plus_icon.rect.collidepoint(*pygame.mouse.get_pos()):
                return const.NEW_LEVEL, level_folder
            elif trash_icon.rect.collidepoint(*pygame.mouse.get_pos()):
                os.remove(level_folder + "/" + level_list[level_nr])
                level_nr -= 1
                level_list = os.listdir(level_folder)
            elif arrow_left.rect.collidepoint(*pygame.mouse.get_pos()):
                prev_level()
            elif arrow_right.rect.collidepoint(*pygame.mouse.get_pos()):
                next_level()
            elif exit_button.rect.collidepoint(*pygame.mouse.get_pos()):
                sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                next_level()
            elif event.key == pygame.K_LEFT:
                prev_level()
            elif event.key == pygame.K_RETURN:
                if level_folder_edit:
                    level_folder = level_folder.replace("Main levels folder", const.MAIN_LEVELS_FOLDER)
                    level_folder = level_folder.replace("User levels folder", const.USER_LEVELS_FOLDER)
                    level_folder_edit = False
                else:
                    return const.PLAY_LEVEL, selected_level()
            elif event.key == pygame.K_BACKSPACE and level_folder_edit:
                if len(level_folder) > 0:
                    level_folder = level_folder[:-1]
            elif event.key == pygame.K_DELETE:
                if level_folder_edit:
                    level_folder = ""
            elif event.key == pygame.K_ESCAPE:
                if not level_folder_edit:
                    sys.exit(0)

            if level_folder_edit and event.key not in (pygame.K_BACKSPACE, pygame.K_RETURN, pygame.K_DELETE):
                level_folder += event.unicode

    screen.fill((50, 0, 25))

    try:
        if not level_folder_edit:
            level_list = os.listdir(level_folder)
            sort_level_list_by_difficulty()
            if len(level_list) != 0:
                level_info = level_files.open_level_data(level_folder + "/" + level_list[level_nr])["info"]
            else:
                level_info = convert.Level()["info"]
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

    if len(level_list) != 0:
        if not levelname_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
            levelname_text = fonts.pusab_big.render(f'{level_nr + 1}/{len(level_list)}) {level_info["name"]}', True,
                                                    (255, 200, 0), (25, 0, 12))
        else:
            levelname_text = fonts.pusab_big.render(f'{level_nr + 1}/{len(level_list)}) {level_info["name"]}', True,
                                                    (0, 255, 0))
    else:
        levelname_text = fonts.pusab_big.render("Current folder is empty!", True, (255, 200, 0), (25, 0, 12))

    difficulty_text = fonts.aller_normal.render(f'Difficulty: {const.DIFFICULTY[int(level_info["stars"])]}, '
                                                f'{level_info["stars"]}*', True, (255, 255, 255))
    creator_text = fonts.aller_normal.render(f'Created by: {level_info["creator"]}', True, (255, 255, 255))
    if current_level_percentage() == 100:
        comp_text = fonts.aller_normal.render(f'{current_level_percentage()}% Completed', True, (100, 255, 100))
    else:
        comp_text = fonts.aller_normal.render(f'{current_level_percentage()}% Completed', True, (255, 100, 100))

    if not level_folder_edit:
        if level_folder == const.MAIN_LEVELS_FOLDER:
            folder_text = fonts.aller_small.render(f'Current levels folder: Main levels folder', True, (255, 255, 255))
        elif level_folder == const.USER_LEVELS_FOLDER:
            folder_text = fonts.aller_small.render(f'Current levels folder: User levels folder', True, (255, 255, 255))
        else:
            folder_text = fonts.aller_small.render(f'Current levels folder: {level_folder}', True, (255, 255, 255))
    else:
        folder_text = fonts.aller_small.render(f'Current levels folder: {level_folder}', True,
                                               (0, 255, 0))

    levelname_rect = levelname_text.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2.7))
    difficulty_rect = difficulty_text.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2))
    creator_rect = creator_text.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 1.8))
    comp_rect = comp_text.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 1.6))
    folder_rect = folder_text.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 1.2))
    error_rect = error_text.get_rect(center=(const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 1.1))

    if not level_folder_edit and not folder_error:
        screen.blit(levelname_text, levelname_rect)
        if len(level_list) != 0:
            screen.blit(difficulty_text, difficulty_rect)
            screen.blit(creator_text, creator_rect)
            screen.blit(comp_text, comp_rect)
            arrow_gr.draw(screen)
    screen.blit(folder_text, folder_rect)
    screen.blit(error_text, error_rect)

    ui_other_gr.draw(screen)

    return const.CONTINUE, selected_level()


def loop(screen: pygame.Surface) -> tuple:
    """
    Loop-Funktion für das Levelmenü, die gdr.level.level_select.loop aufruft, um Fehler abfangen zu können. Falls ein
    Fehler auftritt, wird mit gdr.assets.error_screen.loop die entsprechende Fehlermeldung angezeigt und der Mainloop
    aus gdr.base unterbrochen, bis der Spieler die Maustaste drückt.

    :param screen: pygame.Surface, auf das das Levelmenü gezeichnet werden soll.
    :return: Tupel mit einem Exit-Code als erstes Element und dem Levelnamen als zweites
    (Ausnahmen: (VIEW_SAVE_FILE, None); (NEW_LEVEL, level_folder))
    """

    global level_folder
    try:
        return loop_no_exception(screen)
    except Exception as e:
        while error_screen.loop(screen, str(e)) != const.EXIT:
            pygame.display.update()
        level_folder = const.MAIN_LEVELS_FOLDER
        return loop_no_exception(screen)
