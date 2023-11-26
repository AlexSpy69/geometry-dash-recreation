import geometry_dash_recreation.level as level
import geometry_dash_recreation.convert as convert
from geometry_dash_recreation.constants import *
import pygame
import sys
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HIDDEN)

print("Geometry Dash Level Editor Tool")

current_level = convert.Level()

def iter() -> None:
    global current_level
    inp = input("> ").split()
    if inp[0] == "open":
        current_level = level.open_level_data(inp[1])
    elif inp[0] == "save":
        level.save_level_data(inp[1], current_level)
    elif inp[0] == "add":
        if inp[1] == "comp":
            current_level["sprites"].append(convert.CompSprite(imgfile=inp[2], pos=[int(inp[3]), int(inp[4])],
                                                               size=[int(inp[5]), int(inp[6])], hb_mul=float(inp[7]),
                                                               type=inp[8], color=inp[9]))
    elif inp[0] == "remove":
        if inp[1] == "all":
            for sprite in current_level:
                sprite.kill()
    elif inp[0] == "edit":
        current_level[inp[1]][inp[2]] = inp[3]
    elif inp[0] == "print":
        print(current_level)
    elif inp[0] == "exit":
        sys.exit(0)
    else:
        print("Command not found")

while True:
    try:
        iter()
    except Exception as e:
        print(str(e))
