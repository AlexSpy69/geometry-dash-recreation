from geometry_dash_recreation.level import level, convert
from geometry_dash_recreation.constants import *
import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.HIDDEN)

print("Geometry Dash Level Editor Tool")

current_level = convert.Level()


def execute(command) -> None:
    global current_level
    if command.startswith("#") or command == "\n":
        return
    inp = command.split()
    if inp[0] == "open":
        current_level = level.open_level_data(inp[1].replace("levels/", LEVELS_FOLDER + "/"))
    elif inp[0] == "save":
        level.save_level_data(inp[1].replace("levels/", LEVELS_FOLDER + "/"), current_level)
    elif inp[0] == "add":
        if inp[1] == "comp":
            current_level["sprites"].append(convert.CompSprite(imgfile=f"{ASSETS_FOLDER}/textures/components/{inp[2]}",
                                                               pos=[float(inp[3]), float(inp[4])], size=[float(inp[5]),
                                                                                                         float(inp[6])],
                                                               angle=float(inp[7]), hb_mul=float(inp[8]), type_=inp[9], color=inp[10]))
    elif inp[0] == "remove":
        if inp[1] == "all":
            current_level["sprites"] = []
    elif inp[0] == "edit":
        current_level[inp[1].replace("levels/", LEVELS_FOLDER + "/")][inp[2]] = inp[3].replace("_", " ")
    elif inp[0] == "print":
        print(current_level)
    elif inp[0] == "exit":
        sys.exit(0)
    else:
        print("Command not found")


if len(sys.argv) == 1:
    while True:
        try:
            execute(input("> "))
        except Exception as e:
            print(str(e))
else:
    if sys.argv[1] == "script":
        with open(sys.argv[2]) as f:
            for line in f.readlines():
                try:
                    execute(line)
                except Exception as e:
                    print(str(e))
                    break
