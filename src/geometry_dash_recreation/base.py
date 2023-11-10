import pygame
from pygame.locals import *
from geometry_dash_recreation.constants import *
import geometry_dash_recreation.sprites as sprites
import geometry_dash_recreation.controls as controls

# Pygame-Initialisierung
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Spielfenster
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash Recreation")

# Sprites
cube = sprites.Cube()
player_spr = pygame.sprite.GroupSingle(cube)

event = False
click = False
gravity = 1

mode = "game"

# Diese Funktion wird von main_loop() aufgerufen, wenn der Spieler gerade im Spiel ist.
def game_func() -> None:
    global mode
    for event in pygame.event.get():
        if event.type == QUIT:
            mode = "exit"
    
    player_spr.draw(screen)

# Die Mainloop-Funktion, die in jedem Frame aufgerufen wird und für bestimmte
# Ereignisse einen Exit-Code zurückgibt.
def main_loop() -> int:
    global mode
    match mode:
        case "game":
            game_func()
        case "exit":
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
        pygame.display.flip()
        clock.tick(FPS)

def main():
    main_proc()
