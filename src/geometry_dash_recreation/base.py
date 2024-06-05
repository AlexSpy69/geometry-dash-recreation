"""Dieses Modul ist das Hauptprogramm des Spiels, in dem alle anderen Module "zusammengefügt" werden, um das gesamte
Spiel zu erzeugen."""

import pygame
from pygame.locals import *
from geometry_dash_recreation.constants import *

# Pygame-Initialisierung
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Spielfenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN if FULLSCREEN else 0)
pygame.display.set_caption("Geometry Dash Recreation")

from geometry_dash_recreation.assets import game_sprites, ui_sprites, fonts, screens, error_screen
from geometry_dash_recreation.level import level_files, level_select, convert
from geometry_dash_recreation.save_file import save_file, view_save_file
from geometry_dash_recreation.level_editor import editor, level_properties

# Sprites
background = game_sprites.Background()  # Der Hintergrund, der sich nach links bewegt.
background_2 = game_sprites.Background()  # Ein zweiter Hintergrund-Sprite, der dazu verwendet wird,
# den Hintergrund durchgängig erscheinen zu lassen.
bg_2_front = False
ground = game_sprites.Ground()  # Der "Boden" im Spiel.
ceiling = game_sprites.Ceiling()
bg_gr = pygame.sprite.Group(background_2, background,
                            ground, ceiling)  # Die Group, in der der Boden und der Hintergrund stehen.

cube = game_sprites.Cube()  # Der Cube-Sprite im Spiel
ship = game_sprites.Ship()  # Der Ship-Sprite im Spiel
ball = game_sprites.Ball()  # Der Ball-Sprite im Spiel
player_spr = pygame.sprite.GroupSingle(cube)  # Die Spieler-Sprite-"Gruppe", die nur einen Sprite enthalten kann.

pause_button = ui_sprites.PauseButton()
ingame_ui_gr = pygame.sprite.Group(pause_button)

# Screens
pause_screen = screens.return_pause_screen()
win_screen = screens.return_win_screen()

current_percent_text = fonts.pusab_small.render('100%', True, (255, 255, 255))
current_percent_rect = current_percent_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.05))

current_attempt_text = fonts.text_with_outline("Attempt 0", fonts.pusab_big, 3)
current_attempt_rect = current_attempt_text.get_rect(center=ATTEMPT_COUNT_POS)

# Variablen
ev = False  # True, wenn der Spieler die linke Maustaste gedrückt hält, und False, wenn er sie nicht gedrückt hält
click = False  # True, wenn der Spieler die linke Maustaste drückt, wird aber im nächsten Durchgang
# des Mainloops direkt auf False gesetzt
gravity = 1  # Die Richtung der Gravitation: Bei 1 fällt der Spieler nach unten, bei -1 nach oben.
x_to_level = 0

mode = "level select"  # Der "Zustand" des Spiels.

# Save File
current_sf = save_file.open_sf(SAVE_FILE_PATH)
current_sf.update_stats()

# Level
level_gr = pygame.sprite.Group()
level_gr_unconverted = convert.Level()
current_level_name = ""
level_end = 0
level_error_msg = ""
current_attempt = 0

running = True


def change_gamemode(name: str) -> None:
    """
    Ändert den Gamemode im Spiel.

    :param name: Name des Gamemodes (mögliche Werte: "cube", "ball", "ship")
    :return:
    """

    global player_spr, ceiling
    old_y = player_spr.sprite.hitbox.y
    old_vel = player_spr.sprite.vel
    player_spr.add(eval(name))
    player_spr.sprite.hitbox.y = old_y
    player_spr.sprite.vel = old_vel
    if name == "cube":
        ceiling.activated = False
    elif name in ("ship", "ball"):
        ceiling.activated = True
    if ceiling.activated:
        ceiling.rect.bottom = CEILING_HEIGHT
    else:
        ceiling.rect.bottom = 0


def screen_func(surface: pygame.Surface) -> None:
    """
    Zeigt ein pygame.Surface auf dem Bildschirm an und wartet, bis der Spieler eine Taste oder die Maustaste drückt.

    :param surface: Das pygame.Surface, das auf dem Bildschirm angezeigt werden soll
    :return:
    """

    clicked = False
    screen.blit(surface, (0, 0))
    pygame.display.flip()
    while not clicked:
        for event in pygame.event.get():
            if event.type == QUIT:
                clicked = True
            if event.type == MOUSEBUTTONDOWN or \
                    event.type == KEYDOWN:
                clicked = True


def get_current_level_percent() -> int:
    """
    Liefert den Prozentsatz des Verhältnisses zwischen der Weite, die der Spieler im aktuellen Level erreicht hat,
    und der Länge des Levels.

    :return: Der Prozentsatz
    """

    global x_to_level, level_end
    return int(x_to_level / level_end * 100)


def game_func() -> None:
    """
    Funktion mit einem Mainloop-Durchgang für das richtige Spielen.

    :return:
    """

    global mode, ev, click, gravity, level_gr, level_gr_unconverted, x_to_level, level_end, bg_2_front, current_attempt
    global current_percent_text, current_percent_rect, current_attempt_text, current_attempt_rect
    for event in pygame.event.get():
        if event.type == QUIT:
            mode = "level select"
        elif event.type == MOUSEBUTTONDOWN:
            if pause_button.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                screen_func(pause_screen)
                continue
            ev = True
            click = True
        elif event.type == MOUSEBUTTONUP:
            ev = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                ev = True
                click = True
            if event.key == K_ESCAPE:
                screen_func(pause_screen)
                continue
        elif event.type == KEYUP:
            if event.key == K_SPACE or event.key == K_UP:
                ev = False

    # Überprüfen, ob der Spieler das Levelende erreicht hat
    x_to_level += LEVEL_SCROLL_SPEED / UNIT

    if x_to_level >= level_end:
        mode = "win"

    if player_spr.sprite.hitbox.right < PLAYER_X:
        player_spr.sprite.hitbox.right += LEVEL_SCROLL_SPEED
    else:
        # Bewegen der Level-Komponenten
        for sprite in level_gr:
            sprite.rect.x -= LEVEL_SCROLL_SPEED
            sprite.hitbox.center = sprite.rect.center

        # Bewegen des Hintergrunds
        background.rect.x -= BACKGROUND_SCROLL_SPEED

        # Bewegen des Attempt-Labels
        if current_attempt_rect.right > 0:
            current_attempt_rect.x -= LEVEL_SCROLL_SPEED

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

    # Kontrolle des Spielers
    controls = player_spr.sprite.controls(ev, click, gravity, ground, ceiling, level_gr, level_gr_unconverted)

    if controls == NORMAL:
        pass
    elif controls == DEATH:
        mode = "death"
    elif controls == WIN:
        mode = "win"
    elif controls == CHANGE_GRAVITY:
        gravity = gravity * -1
    elif controls == CUBE_GAMEMODE:
        change_gamemode("cube")
    elif controls == SHIP_GAMEMODE:
        change_gamemode("ship")
    elif controls == BALL_GAMEMODE:
        change_gamemode("ball")

    click = False

    bg_gr.update()
    level_gr.update()
    player_spr.update()

    current_percent_text = fonts.pusab_small.render(f"{get_current_level_percent()}%", True, (255, 255, 255))
    current_percent_rect = current_percent_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.05))

    current_attempt_text = fonts.text_with_outline(f"Attempt {current_attempt}", fonts.pusab_big, 3)

    screen.fill((0, 0, 0))
    for bg in background, background_2:
        screen.blit(bg.image, bg.rect)
    level_gr.draw(screen)
    for gr in ground, ceiling:
        screen.blit(gr.image, gr.rect)
    player_spr.draw(screen)
    ingame_ui_gr.draw(screen)
    screen.blit(current_percent_text, current_percent_rect)
    if current_attempt_rect.right > 0:
        screen.blit(current_attempt_text, current_attempt_rect)


def get_level_end() -> int:
    """
    Berechnet und liefert das Ende des aktuellen Levels, das in der globalen Variable level_gr_unconverted
    gespeichert ist.

    :return: Entfernung zwischen dem Anfang und dem Ende des Levels in Levelblockweiten (gdr.constants.UNIT)
    """

    global level_gr_unconverted
    max_value = 0
    for sprite in level_gr_unconverted["sprites"]:
        if sprite["pos"][0] > max_value:
            max_value = sprite["pos"][0]
    return max_value + 10


def init_level() -> str:
    """
    Initialisiert das Level mit dem Dateinamen in der globalen Variable current_level_name.

    :return:
    """

    global mode, level_gr, level_gr_unconverted, player_spr, ev, click, \
        gravity, current_level_name, x_to_level, level_end, current_attempt_rect, current_attempt

    def proc() -> None:
        global mode, level_gr, level_gr_unconverted, player_spr, ev, click, \
            gravity, current_level_name, x_to_level, level_end, current_attempt_rect, current_attempt

        # Leveldaten
        level_gr_unconverted = level_files.open_level_data(current_level_name)
        level_gr = convert.data_to_group(level_gr_unconverted)

        # Sprites
        background.reset()
        background_2.reset()

        # Level
        level_end = get_level_end()

        # Gamemode
        change_gamemode(level_gr_unconverted["data"]["gamemode"])
        player_spr.sprite.reset()

        # Physik
        ev, click, gravity = False, False, 1
        x_to_level = 0

        # Attempt
        current_attempt += 1
        current_attempt_rect.center = ATTEMPT_COUNT_POS

    try:
        proc()
    except Exception as e:
        return str(e)

    return ""


def level_error() -> None:
    """
    Hauptschleifen-Durchgang für den Level-Error-Screen (gdr.error_screen.loop). Es wird die Fehlermeldung in der
    globalen Variable level_error_msg engezeigt. Die globale Variable mode wird bei dem Schließen des Screens auf
    "level select" gesetzt.

    mode-Wert: "level error"

    :return:
    """

    global mode, level_error_msg
    error_scr = error_screen.loop(screen, level_error_msg)
    if error_scr == CONTINUE:
        pass
    elif error_scr == EXIT:
        mode = "level select"


def level_select_func() -> None:
    """
    Hauptschleifen-Durchgang für das Levelmenü (gdr.level.level_select.loop). Die globale Variable mode kann zu
    folgenden Werten geändert werden: "view save file", "level editor", "init level", "new level".

    mode-Wert: "level select"

    :return:
    """

    global mode, current_level_name, current_attempt
    current_attempt = 0

    level_screen = level_select.loop(screen)

    if level_screen[0] == CONTINUE:
        current_level_name = level_screen[1]
    elif level_screen[0] == VIEW_SAVE_FILE:
        mode = "view save file"
    elif level_screen[0] == OPEN_LEVEL_EDITOR:
        init_level()
        mode = "level editor"
    elif level_screen[0] == PLAY_LEVEL:
        mode = "init level"
    elif level_screen[0] == NEW_LEVEL:
        mode = "new level"


def view_save_file_func() -> None:
    """
    Hauptschleifen-Durchgang für den Save-File-Viewer (gdr.save_file.view_save_file.loop). Die globale Variable mode
    wird bei dem Schließen des Viewers auf "level select" gesetzt.

    mode-Wert: "view save file"

    :return:
    """

    global mode
    savefile_screen = view_save_file.loop(screen, current_sf)
    if savefile_screen == CONTINUE:
        pass
    elif savefile_screen == EXIT:
        mode = "level select"


def level_editor_func() -> None:
    """
    Hauptschleifen-Durchgang für den Level-Editor (gdr.level_editor.editor.loop). Die globale Variable mode wird bei dem
    Schließen des Editors auf "level select" gesetzt.

    mode-Wert: "level editor"

    :return:
    """

    global mode, level_gr
    exit_code, level_group = editor.loop(screen, level_gr, level_gr_unconverted,
                                         bg_gr, background, background_2,
                                         level_select.level_folder)

    if exit_code == CONTINUE:
        pass
    elif exit_code == SAVE_LEVEL:
        level_gr = level_group
        level_gr_unconverted["sprites"] = convert.group_to_data(level_gr, True)
        level_files.save_level_data(current_level_name, level_gr_unconverted)
    elif exit_code == SAVE_LEVEL_PROPERTIES:
        level_gr_unconverted["info"], level_gr_unconverted["data"] = \
            level_group["info"], level_group["data"]
        level_files.save_level_data(current_level_name, level_gr_unconverted)
    elif exit_code == EXIT:
        mode = "level select"


def new_level_func() -> None:
    """
    Hauptschleifen-Durchgang für das Menü zum Erstellen einer neuen Leveldatei (gdr.level_editor.level_properties.loop).
    Die globale Variable mode wird bei dem Schließen des Editors auf "level select" gesetzt.

    mode-Wert: "new level"

    :return:
    """

    global mode
    lp = level_properties.loop(screen, level_select.level_folder, "create")

    if lp == CONTINUE:
        pass
    elif lp == EXIT:
        mode = "level select"


def main_loop() -> int:
    """
    Die Funktion, die in jedem Frame in der Funktion gdr.base.main_proc einmal aufgerufen wird und für verschiedene
    Werte der globalen Variable mode die richtige Hauptschleifen-Durchgangs-Funktion ausführt

    :return: Exit-Code (gdr.constants.CONTINUE oder gdr.constants.EXIT)
    """

    global mode, level_error_msg, level_end, x_to_level
    match mode:
        case "game":
            game_func()
        case "level select":
            level_select_func()
        case "view save file":
            view_save_file_func()
        case "level editor":
            level_editor_func()
        case "new level":
            new_level_func()
        case "exit":
            return EXIT
        case "init level":
            level_error_msg = init_level()
            if level_error_msg != "":
                mode = "level error"
            else:
                mode = "game"
        case "level error":
            level_error()
        case "death":
            if get_current_level_percent() > current_sf.get_level_percent(current_level_name):
                current_sf.set_level(current_level_name, get_current_level_percent())
            save_file.save_sf(current_sf, SAVE_FILE_PATH)
            pygame.time.wait(500)
            mode = "init level"
        case "win":
            current_sf.set_level(current_level_name, 100)
            current_sf.update_stats()
            save_file.save_sf(current_sf, SAVE_FILE_PATH)
            screen_func(win_screen)
            mode = "level select"

    return CONTINUE


def main_process() -> None:
    """
    Die Hauptfunktion, die nur einmal bei dem Starten des Spiels von der Funktion gdr.base.main aufgerufen wird und
    das ganze Spiel lang läuft. Hier befindet sich die Hauptschleife des Spiels, in der die Funktion gdr.base.main_loop
    aufgerufen wird.

    :return:
    """

    global running
    clock = pygame.time.Clock()
    while running:
        ml = main_loop()
        if ml == CONTINUE:
            pass
        elif ml == EXIT:
            running = False
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


def main():
    """
    Die Funktion, die von gdr.__main__ aufgerufen wird und selbst gdr.base.main_process aufruft.

    :return:
    """

    main_process()
