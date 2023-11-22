import pygame
from pygame.locals import *
from geometry_dash_recreation.constants import *
import geometry_dash_recreation.sprites as sprites
import geometry_dash_recreation.level as level
import geometry_dash_recreation.convert as convert

# Pygame-Initialisierung
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Spielfenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Geometry Dash Recreation")

# Sprites
background = sprites.Background()                # Der Hintergrund, der sich nach links bewegt.
ground = sprites.Ground()                        # Der "Boden" im Spiel.
bg_gr = pygame.sprite.Group(background, ground)  # Die Group, in der der Boden und der Hintergrund stehen.

cube = sprites.Cube()                          # Der Cube-Sprite im Spiel
player_spr = pygame.sprite.GroupSingle(cube)   # Die Spieler-Sprite-"Gruppe", die nur einen Sprite enthalten kann.

ev = False     # True, wenn der Spieler die linke Maustaste gedrückt hält, und False, wenn er sie nicht gedrückt hält
click = False  # True, wenn der Spieler die linke Maustaste drückt, wird aber im nächsten Durchgang der Mainloop direkt auf False gesetzt
gravity = 1    # Die Richtung der Gravitation: Bei 1 fällt der Spieler nach unten, bei -1 nach oben.

mode = "set level"  # Der "Zustand" des Spiels.

# Level
#level.save_level_data("levels/start", level.convert.Level())
level_gr_unconverted = level.open_level_data(START_LEVEL)
print(level_gr_unconverted)
level_gr = convert.data_to_group(level_gr_unconverted)  # Group mit allen Objekten im Level.
level_error_msg = ""

# Diese Funktion wird von main_loop() aufgerufen, wenn der Spieler gerade im Spiel ist.
def game_func() -> None:
    global mode, ev, click, gravity
    for event in pygame.event.get():
        if event.type == QUIT:
            mode = "exit"
        elif event.type == MOUSEBUTTONDOWN:
            ev = True
            click = True
        elif event.type == MOUSEBUTTONUP:
            ev = False
    
    match player_spr.sprite.controls(ev, click, gravity, ground, level_gr):
        case 0:
            pass
        case 1:
            mode = "death"
    
    click = False

    bg_gr.update()
    level_gr.update()
    player_spr.update()
    
    bg_gr.draw(screen)
    level_gr.draw(screen)
    player_spr.draw(screen)

def set_level() -> str:
    def proc() -> None:
        global mode, level_gr, player_spr, ev, click, gravity
        # Gamemode
        exec(f"player_spr.add({level_gr_unconverted['data']['gamemode']})")
        # Physik
        ev, click, gravity = False, False, 1
    
    try:
        proc()
    except Exception as e:
        return str(e)
    
    return ""

def level_error() -> None:
    global mode, level_error_msg
    print(level_error_msg)
    mode = "exit"

# Die Mainloop-Funktion, die in jedem Frame aufgerufen wird und für bestimmte
# Ereignisse einen Exit-Code zurückgibt.
def main_loop() -> int:
    global mode, level_error_msg
    match mode:
        case "game":
            game_func()
        case "exit":
            return 1
        case "set level":
            level_error_msg = set_level()
            if level_error_msg != "":
                mode = "level error"
            else:
                mode = "game"
        case "level error":
            level_error()
        case "death":
            return 1
    
    return 0

# Die Hauptfunktion, die nur einmal aufgerufen wird. Der while-Loop ruft
# die Mainloop-Funktion auf und verwaltet ihre Exit-Codes.
def main_proc() -> None:
    clock = pygame.time.Clock()
    while True:
        match main_loop():
            case 0:
                pass
            case 1:
                break
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()

# Die FUnktion, die von __main__.py  aufgerufen wird.
def main():
    main_proc()
