import pygame
from pygame.locals import *
from geometry_dash_recreation.constants import *
import geometry_dash_recreation.sprites as sprites
import geometry_dash_recreation.level as level
import geometry_dash_recreation.convert as convert
import geometry_dash_recreation.level_select as level_select

# Pygame-Initialisierung
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Spielfenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Geometry Dash Recreation")

# Sprites
background = sprites.Background()                # Der Hintergrund, der sich nach links bewegt.
background_2 = sprites.Background()              # Ein zweiter Hintergrund-Sprite, der dazu verwendet wird,
                                                 # den Hintergrund durchgängig erscheinen zu lassen.
bg_2_front = False
ground = sprites.Ground()                        # Der "Boden" im Spiel.
ceiling = sprites.Ceiling()
bg_gr = pygame.sprite.Group(background_2, background,
                            ground, ceiling)   # Die Group, in der der Boden und der Hintergrund stehen.

cube = sprites.Cube()                          # Der Cube-Sprite im Spiel
ship = sprites.Ship()                          # Der Ship-Sprite im Spiel
ball = sprites.Ball()                          # Der Ball-Sprite im Spiel
player_spr = pygame.sprite.GroupSingle(cube)   # Die Spieler-Sprite-"Gruppe", die nur einen Sprite enthalten kann.

pause_button = sprites.PauseButton()
ingame_ui_gr = pygame.sprite.Group(pause_button)

# Screens
pause_screen = pygame.transform.scale(
    pygame.image.load("assets/textures/ui/pause_screen.png").convert_alpha(),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

win_screen = pygame.transform.scale(
    pygame.image.load("assets/textures/ui/win_screen.png").convert_alpha(),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# Variablen
ev = False     # True, wenn der Spieler die linke Maustaste gedrückt hält, und False, wenn er sie nicht gedrückt hält
click = False  # True, wenn der Spieler die linke Maustaste drückt, wird aber im nächsten Durchgang der Mainloop direkt auf False gesetzt
gravity = 1    # Die Richtung der Gravitation: Bei 1 fällt der Spieler nach unten, bei -1 nach oben.
x_to_level = 0

mode = "level select"  # Der "Zustand" des Spiels.

# Level
#level.save_level_data("levels/start", level.convert.Level())""
level_gr = pygame.sprite.Group()
level_gr_unconverted = convert.Level()
current_level_name = ""
level_end = 0

def change_gamemode(name: str, init: bool = False) -> None:
    global player_spr, ceiling
    old_y = player_spr.sprite.hitbox.y
    old_vel = player_spr.sprite.vel
    exec(f"player_spr.add({name})")
    player_spr.sprite.hitbox.y = old_y
    player_spr.sprite.vel = old_vel
    if name == "cube":
        ceiling.activated = False
    elif name in ("ship", "ball"):
        ceiling.activated = True
    if init:
        if ceiling.activated:
            ceiling.rect.bottom = CEILING_HEIGHT
        else:
            ceiling.rect.bottom = 0

def screen_func(surface: pygame.Surface) -> None:
    global mode
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

# Diese Funktion wird von main_loop() aufgerufen, wenn der Spieler gerade im Spiel ist.
def game_func() -> None:
    global mode, ev, click, gravity, level_gr, level_gr_unconverted, x_to_level, level_end, bg_2_front
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
    
    x_to_level += LEVEL_SCROLL_SPEED / UNIT

    if x_to_level >= level_end:
        mode = "win"

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

    background.rect.x -= BACKGROUND_SCROLL_SPEED

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

    bg_gr.update()
    level_gr.update()
    player_spr.update()
    
    screen.fill((0, 0, 0))
    bg_gr.draw(screen)
    level_gr.draw(screen)
    player_spr.draw(screen)
    ingame_ui_gr.draw(screen)

# Wird aufgerufen, um das Level zu initialisieren
def init_level() -> str:
    global mode, level_gr, level_gr_unconverted, player_spr, ev, click, \
        gravity, current_level_name, x_to_level, level_end
    
    def max_x() -> int:
        global level_gr_unconverted
        max_value = 0
        for sprite in level_gr_unconverted["sprites"]:
            if sprite["pos"][0] > max_value:
                max_value = sprite["pos"][0]
        
        return max_value

    def proc() -> None:
        global mode, level_gr, level_gr_unconverted, player_spr, ev, click, \
            gravity, current_level_name, x_to_level, level_end
        level_gr_unconverted = level.open_level_data(current_level_name)
        level_gr = convert.data_to_group(level_gr_unconverted)
        # Sprites
        background.reset()
        background_2.reset()
        # Level
        level_end = max_x() + 10
        # Gamemode
        change_gamemode(level_gr_unconverted["data"]["gamemode"], True)
        player_spr.sprite.reset()
        # Physik
        ev, click, gravity = False, False, 1
        x_to_level = 0
    
    try:
        proc()
    except Exception as e:
        return str(e)
    
    return ""

def level_error() -> None:
    global mode, level_error_msg
    print(level_error_msg)
    mode = "exit"

def lvl_select() -> None:
    global mode, current_level_name
    l = level_select.loop(screen)
    if l != "":
        current_level_name = l
        mode = "init level"

# Die Mainloop-Funktion, die in jedem Frame aufgerufen wird und für bestimmte
# Ereignisse einen Exit-Code zurückgibt.
def main_loop() -> int:
    global mode, level_error_msg
    match mode:
        case "game":
            game_func()
        case "level select":
            lvl_select()
        case "exit":
            return 1
        case "init level":
            level_error_msg = init_level()
            if level_error_msg != "":
                mode = "level error"
            else:
                mode = "game"
        case "level error":
            level_error()
        case "death":
            pygame.time.wait(500)
            mode = "init level"
        case "win":
            screen_func(win_screen)
            mode = "level select"
    
    return 0

# Die Hauptfunktion, die nur einmal aufgerufen wird. Der while-Loop ruft
# die Mainloop-Funktion auf und verwaltet ihre Exit-Codes.
def main_proc() -> None:
    global clock
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

# Die Funktion, die von __main__.py  aufgerufen wird.
def main():
    main_proc()
