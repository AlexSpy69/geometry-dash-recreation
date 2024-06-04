import pygame
from geometry_dash_recreation.constants import *
from geometry_dash_recreation.assets import fonts, ui_sprites, screens
from geometry_dash_recreation.level import convert, level_files
from geometry_dash_recreation.save_file import save_file

pygame.init()
pygame.font.init()

exit_button = ui_sprites.ExitButton()
exit_button.rect.x, exit_button.rect.y = SCREEN_WIDTH * 0.91, SCREEN_HEIGHT * 0.03

name_text = fonts.aller_small.render(f"Level name: ", True, (255, 255, 255))
name_rect = name_text.get_rect(center=(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.3))

creator_text = fonts.aller_small.render(f"Creator: ", True, (255, 255, 255))
creator_rect = name_text.get_rect(center=(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.4))

stars_text = fonts.aller_small.render(f"Stars: ", True, (255, 255, 255))
stars_rect = name_text.get_rect(center=(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.5))

gamemode_text = fonts.aller_small.render(f"Starting gamemode: ", True, (255, 255, 255))
gamemode_rect = name_text.get_rect(center=(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.6))

go_text = fonts.pusab_big.render("Create level", True, (255, 255, 255))
go_rect = go_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))

transparent_screen = screens.return_semi_transparent_screen()

name_edit = False
creator_edit = False
stars_edit = False
gamemode_edit = False

name = None
creator = None
stars = None
gamemode = None


def loop(screen: pygame.Surface, level_folder: str, mode: str, transparent: bool = False,
         def_vals: tuple = ("", save_file.open_sf(SAVE_FILE_PATH).playerdata["name"],
                            "", "cube"),
         level_gr_unconverted: convert.Level = None) -> int | convert.Level:
    global name, creator, stars, gamemode
    global name_edit, creator_edit, stars_edit, gamemode_edit
    global name_text, creator_text, stars_text, gamemode_text
    global name_rect, creator_rect, stars_rect, gamemode_rect
    global go_text, go_rect

    if name is None:
        name = def_vals[0]
    if creator is None:
        creator = def_vals[1]
    if stars is None:
        stars = def_vals[2]
    if gamemode is None:
        gamemode = def_vals[3]

    if level_gr_unconverted is None:
        level_gr_unconverted = convert.Level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.rect.collidepoint(*pygame.mouse.get_pos()):
                return EXIT
            elif name_rect.collidepoint(*pygame.mouse.get_pos()):
                name_edit, creator_edit, stars_edit, gamemode_edit = True, False, False, False
            elif creator_rect.collidepoint(*pygame.mouse.get_pos()):
                name_edit, creator_edit, stars_edit, gamemode_edit = False, True, False, False
            elif stars_rect.collidepoint(*pygame.mouse.get_pos()):
                name_edit, creator_edit, stars_edit, gamemode_edit = False, False, True, False
            elif gamemode_rect.collidepoint(*pygame.mouse.get_pos()):
                name_edit, creator_edit, stars_edit, gamemode_edit = False, False, False, True
            elif go_rect.collidepoint(*pygame.mouse.get_pos()):
                if mode == "create":
                    r = convert.Level()
                    r["info"]["name"], r["info"]["creator"], r["info"]["stars"], r["data"]["gamemode"] = \
                        name, creator, stars, gamemode
                    level_files.save_level_data(level_folder + "/" + name, r)
                    return EXIT
                elif mode == "edit":
                    level_gr_unconverted["info"]["name"], level_gr_unconverted["info"]["creator"], \
                        level_gr_unconverted["info"]["stars"], level_gr_unconverted["data"]["gamemode"] = \
                        name, creator, stars, gamemode.lower()
                    return level_gr_unconverted
        elif event.type == pygame.KEYDOWN:
            if event.key not in (pygame.K_BACKSPACE, pygame.K_RETURN):
                if name_edit:
                    name += event.unicode
                elif creator_edit:
                    creator += event.unicode
                elif stars_edit:
                    stars += event.unicode
                elif gamemode_edit:
                    gamemode += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                if name_edit:
                    if len(name) > 0:
                        name = name[:-1]
                elif creator_edit:
                    if len(creator) > 0:
                        creator = creator[:-1]
                elif stars_edit:
                    if len(stars) > 0:
                        stars = stars[:-1]
                elif gamemode_edit:
                    if len(gamemode) > 0:
                        gamemode = gamemode[:-1]

    name_text = fonts.aller_small.render(f"Level name: {name}", True, (0, 255, 0) if name_edit else (255, 255, 255))

    creator_text = fonts.aller_small.render(f"Creator: {creator}", True,
                                            (0, 255, 0) if creator_edit else (255, 255, 255))

    stars_text = fonts.aller_small.render(f"Stars: {stars}", True, (0, 255, 0) if stars_edit else (255, 255, 255))

    gamemode_text = fonts.aller_small.render(f"Starting gamemode: {gamemode}", True,
                                             (0, 255, 0) if gamemode_edit else (255, 255, 255))

    go_text = fonts.pusab_big.render("Save new properties" if mode == "edit" else "Create empty level file", True,
                                     (0, 255, 0) if go_rect.collidepoint(*pygame.mouse.get_pos()) else (255, 255, 255))
    go_rect = go_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.8))

    if transparent:
        screen.blit(transparent_screen, (0, 0))
    else:
        screen.fill((50, 0, 25))
    screen.blit(name_text, name_rect)
    screen.blit(creator_text, creator_rect)
    screen.blit(stars_text, stars_rect)
    screen.blit(gamemode_text, gamemode_rect)
    screen.blit(go_text, go_rect)

    screen.blit(exit_button.image, exit_button.rect)

    return CONTINUE
