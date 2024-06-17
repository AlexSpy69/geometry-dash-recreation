"""Dieses Modul ist für den Save-File-Viewer zuständig."""

import sys
import pygame
from geometry_dash_recreation import constants as const
from geometry_dash_recreation.assets import fonts
from geometry_dash_recreation.save_file import save_file
from geometry_dash_recreation.level import level_files

pygame.init()
pygame.font.init()

# text
exit_text = fonts.pusab_small.render('Exit', True, (255, 255, 255))
exit_rect = exit_text.get_rect(center=(const.SCREEN_WIDTH * 0.9, const.SCREEN_HEIGHT * 0.05))

ntext = fonts.aller_small.render('', True, (255, 255, 255))
nrect = ntext.get_rect(center=(const.SCREEN_WIDTH * 0.2, const.SCREEN_HEIGHT * 0.37))

name_edit = False
name_temp = None


def save_name(sf: save_file.SaveFile, name: str) -> None:
    """
    Speichert den Spielernamen in ein SaveFile-Objekt und serialisiert es.

    :param sf: SaveFile-Objekt
    :param name: Spielername
    :return:
    """

    sf.playerdata["name"] = name
    save_file.save_sf(sf, const.SAVE_FILE_PATH)


def render_level_list_element(txt: str, ypos: int, screen: pygame.Surface, color: pygame.Color) -> None:
    """
    Zeichnet ein Element der Level-Liste auf den Bildschirm.

    :param txt: Der Inhalt der Textzeile, die angezeigt werden soll
    :param ypos: y-Position des Textes zu SCREEN_HEIGHT * 0.67 (vordefinierte Position des Starts der Levelliste)
        (wird mit SCREEN_HEIGHT * 0.04 multipliziert)
    :param screen: pygame.Surface, auf das der Text gezeichnet werden soll
    :param color: Die Farbe der Zeile, die angzeigt werden soll
    :return:
    """

    render = fonts.aller_smaller.render(txt, True, color)
    screen.blit(render, render.get_rect(center=(const.SCREEN_WIDTH * 0.5, const.SCREEN_HEIGHT * 0.67 +
                                                const.SCREEN_HEIGHT * 0.04 * ypos)))


def create_level_list_element_text(level_path: str, player_save_file: save_file.SaveFile) -> str:
    """
    Erstellt den Inhalt eines Level-Listen-Elements.

    :param level_path: Der Pfad des Levels
    :param player_save_file: Der Save-File des Spielers
    :return String mit dem Inhalt des zugehörigen Level-Listen-Elements
    """

    if level_path.startswith(const.MAIN_LEVELS_FOLDER):
        return (f'Main levels/{level_path.split("/")[-1]}, '
                f'{level_files.open_level_data(level_path)["info"]["stars"]}*, '
                f'{player_save_file.lvldict[level_path]}%')
    elif level_path.startswith(const.USER_LEVELS_FOLDER):
        return (f'User levels/{level_path.split("/")[-1]}, '
                f'{level_files.open_level_data(level_path)["info"]["stars"]}*, '
                f'{player_save_file.lvldict[level_path]}%')
    elif level_path.startswith(const.HOME_FOLDER):
        return (f'Home folder/{level_path.split("/")[-1]}, '
                f'{level_files.open_level_data(level_path)["info"]["stars"]}*, '
                f'{player_save_file.lvldict[level_path]}%')
    else:
        return (f'{level_path}, '
                f'{level_files.open_level_data(level_path)["info"]["stars"]}, '
                f'{player_save_file.lvldict[level_path]}%')


def loop(screen: pygame.Surface, sf: save_file.SaveFile) -> int:
    """
    Die Loop-Funktion des Save-File-Viewers.

    :param screen: Der pygame.Surface, auf den der Viewer gezeichnet werden soll
    :param sf: Das SaveFile-Objekt, dessen Inhalt angezeigt werden soll
    :return: Exit-Code
    """

    global exit_text, exit_rect, ntext, nrect
    global name_edit, name_temp

    if name_temp is None:
        name_temp = sf.playerdata["name"]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(*pygame.mouse.get_pos()):
                return const.EXIT
            elif nrect.collidepoint(*pygame.mouse.get_pos()):
                name_edit = not name_edit
                if not name_edit:
                    save_name(sf, name_temp)
        elif event.type == pygame.KEYDOWN:
            if event.key not in (pygame.K_BACKSPACE, pygame.K_RETURN):
                if name_edit:
                    name_temp += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                if name_edit:
                    if len(name_temp) > 0:
                        name_temp = name_temp[:-1]

    if not exit_rect.collidepoint(*pygame.mouse.get_pos()):
        exit_text = fonts.pusab_small.render('Exit', True, (255, 200, 0), (25, 0, 12))
    else:
        exit_text = fonts.pusab_small.render('Exit', True, (0, 255, 0))

    pdtext = fonts.aller_normal.render('Player Data', True, (255, 255, 255))
    pdrect = pdtext.get_rect(center=(const.SCREEN_WIDTH * 0.2, const.SCREEN_HEIGHT * 0.3))

    ntext = fonts.aller_small.render(f'Name: {name_temp}', True, (0, 255, 0) if name_edit else (255, 200, 0))
    nrect = ntext.get_rect(center=(const.SCREEN_WIDTH * 0.2, const.SCREEN_HEIGHT * 0.37))

    pstext = fonts.aller_normal.render('Player Stats', True, (255, 255, 255))
    psrect = pstext.get_rect(center=(const.SCREEN_WIDTH * 0.6, const.SCREEN_HEIGHT * 0.3))

    stext = fonts.aller_small.render(f'Stars: {sf.playerstats["stars"]}*', True, (255, 255, 255))
    srect = stext.get_rect(center=(const.SCREEN_WIDTH * 0.6, const.SCREEN_HEIGHT * 0.37))

    ltext = fonts.aller_normal.render('Played Levels', True, (255, 255, 255))
    lrect = ltext.get_rect(center=(const.SCREEN_WIDTH * 0.5, const.SCREEN_HEIGHT * 0.6))

    lotext = fonts.aller_normal.render(const.SAVE_FILE_PATH, True, (255, 255, 255))
    lorect = lotext.get_rect(center=(const.SCREEN_WIDTH * 0.5, const.SCREEN_HEIGHT * 0.1))

    screen.fill((50, 0, 25))
    screen.blit(exit_text, exit_rect)
    screen.blit(pdtext, pdrect)
    screen.blit(ntext, nrect)
    screen.blit(pstext, psrect)
    screen.blit(stext, srect)
    screen.blit(ltext, lrect)
    screen.blit(lotext, lorect)

    counter = 0
    for lvlname in sf.lvldict.keys():
        red_color = False
        try:
            txt = create_level_list_element_text(lvlname, sf)
        except FileNotFoundError:
            txt = f'Deleted level: {lvlname}, {sf.lvldict[lvlname]}%'
            red_color = True
        render_level_list_element(txt, counter, screen,
                                  pygame.Color(255, 100, 100) if red_color else pygame.Color(255, 255, 255))
        counter += 1

    if counter == 0:
        render_level_list_element("None", 0, screen, pygame.Color(255, 255, 255))

    return const.CONTINUE
