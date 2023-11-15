import geometry_dash_recreation.level as level
import geometry_dash_recreation.sprites as sprites
from geometry_dash_recreation.constants import *
import pygame
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HIDDEN)

print("Geometry Dash Level Editor Tool")

current_level = level.LevelGroup()

def iter() -> None:
    global current_level
    inp = input("> ").split()
    if inp[0] == "open":
        current_level = level.open_level(inp[1])
    elif inp[0] == "save":
        level.save_level(inp[1], current_level)
    elif inp[0] == "add":
        if inp[1] == "comp":
            comp = sprites.Component(imgfile=inp[4], xsize=int(inp[5]),
                                     ysize=int(inp[6]), hb_mul=int(inp[7]))
            comp.rect.x, comp.rect.y = int(inp[2])*UNIT, int(inp[3])*UNIT
            current_level.add(comp)
    elif inp[0] == "remove":
        if inp[1] == "all":
            for sprite in current_level:
                sprite.kill()
    elif inp[0] == "edit":
        if inp[1] == "info":
            current_level.info[inp[2]] = inp[3]
        if inp[1] == "data":
            current_level.data[inp[2]] = inp[3]
    else:
        print("Command not found")

while True:
    try:
        iter()
    except Exception as e:
        print(str(e))
