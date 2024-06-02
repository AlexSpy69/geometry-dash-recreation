import sys

import pygame
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import fonts
from geometry_dash_recreation.save_file import save_file

pygame.init()
pygame.font.init()

# text
exit_text = fonts.pusab_small.render('Exit', True, (255, 255, 255))
exit_rect = exit_text.get_rect(center=(SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.05))

ntext = fonts.aller_small.render('', True, (255, 255, 255))
nrect = ntext.get_rect(center=(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.37))

name_edit = False
name_temp = None


def save_name(sf: save_file.SaveFile, name: str):
    sf.playerdata["name"] = name
    save_file.save_sf(sf, SAVE_FILE_PATH)


def render_level_list(txt, pos, screen) -> None:
    render = fonts.aller_smaller.render(txt, True, (255, 255, 255))
    screen.blit(render, render.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.67 +
                                                SCREEN_HEIGHT * 0.04 * pos)))


def loop(screen: pygame.Surface, sf: save_file.SaveFile) -> int:
    global exit_text, exit_rect, ntext, nrect
    global name_edit, name_temp

    if name_temp == None:
        name_temp = sf.playerdata["name"]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(*pygame.mouse.get_pos()):
                return EXIT
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
    pdrect = pdtext.get_rect(center=(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.3))

    ntext = fonts.aller_small.render(f'Name: {name_temp}', True, (0, 255, 0) if name_edit else (255, 200, 0))
    nrect = ntext.get_rect(center=(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.37))

    pstext = fonts.aller_normal.render('Player Stats', True, (255, 255, 255))
    psrect = pstext.get_rect(center=(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.3))

    stext = fonts.aller_small.render(f'Stars: {sf.playerstats["stars"]}*', True, (255, 255, 255))
    srect = stext.get_rect(center=(SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.37))

    ltext = fonts.aller_normal.render('Played Levels', True, (255, 255, 255))
    lrect = ltext.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6))

    lotext = fonts.aller_normal.render(SAVE_FILE_PATH, True, (255, 255, 255))
    lorect = lotext.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.1))
    
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
        if lvlname.startswith(LEVELS_FOLDER):
            txt = f'Default levels/{lvlname.split("/")[-1]}, {sf.lvldict[lvlname]}%'
        elif lvlname.startswith(HOME_FOLDER):
            txt = f'{lvlname.strip(HOME_FOLDER)}, {sf.lvldict[lvlname]}%'
        else:
            txt = f'{lvlname}, {sf.lvldict[lvlname]}%'
        render_level_list(txt, counter, screen)
        counter += 1

    if counter == 0:
        render_level_list("None", 0, screen)

    return CONTINUE
