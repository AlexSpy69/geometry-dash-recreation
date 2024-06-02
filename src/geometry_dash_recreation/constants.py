import screeninfo
from pathlib import Path
import pkg_resources
import sys
from geometry_dash_recreation import util


def adapt_res(width, height) -> tuple:
    if width/height != 16/9:
        height = int(width * 9/16)
    return width, height

try:
    width, height = map(int, sys.argv[1:3])
    FULLSCREEN = False
except (ValueError, IndexError):
    try:
        MONITOR_NR = int(sys.argv[1])
    except (ValueError, IndexError):
        MONITOR_NR = 0
    width = screeninfo.get_monitors()[MONITOR_NR].width
    height = screeninfo.get_monitors()[MONITOR_NR].height
    width, height = adapt_res(width, height)
    FULLSCREEN = True


# Home-Ordner
HOME_FOLDER = str(Path.home())

# Ressourcen-Ordner
ASSETS_FOLDER = pkg_resources.resource_filename("geometry_dash_recreation", "assets")
LEVELS_FOLDER = pkg_resources.resource_filename("geometry_dash_recreation", "levels")

# Ingame-Konstanten
FPS = 60                        # Bilder pro Sekunde
DELTA_TIME = 60 / FPS           # Abstand zwischen zwei Frames in Sekunden multipliziert mit 60
SCREEN_WIDTH = width            # Fensterbreite
SCREEN_HEIGHT = height          # Fensterhöhe
RESIZE = SCREEN_HEIGHT/1080
UNIT = SCREEN_HEIGHT * 0.08     # Einheit
GROUND_HEIGHT = UNIT * 10       # Höhe des Bodens
CEILING_HEIGHT = UNIT * 1       # Höhe der Decke
CEILING_MOVE = CEILING_HEIGHT/5
PLAYER_X = UNIT * 7             # Ursprüngliche Position des Spielers auf dem Bildschirm
PLAYER_Y = GROUND_HEIGHT
VEL_ADD = 2                     # Stärke der Einwirkung der Gravitation
JUMP_VEL = 27                   # Stärke des Sprungs des Spielers
LEVEL_SCROLL_SPEED = DELTA_TIME*13*RESIZE  # Die Geschwindigkeit, mit der die Objekte in einem Level nach links scrollen
BACKGROUND_SCROLL_SPEED = DELTA_TIME*3*RESIZE  # Die Geschwindigkeit, mit der der Hintergrund nach links scrollt
DEATH_ACCURACY = UNIT
OUT_OF_BOUNDS = -6000
ATTEMPT_COUNT_POS = (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.4)

# Mögliche Level-Komponenten-Eigenschaften
COMPONENT_IMGFILE_LIST = tuple(sorted(util.list_files(ASSETS_FOLDER + "/textures/components", ".png")))
#COMPONENT_TYPE_LIST = ("", "platform", "hazard", "ring", "pad", "formportal", "gravityportal", "deco")
COMPONENT_TYPE_LIST = ("", "platform", "hazard", "ring", "pad", "formportal", "deco")
COMPONENT_COLOR_LIST = ("", "magenta", "yellow", "red", "cyan", "green")

# vel wird bei der Berührung von bestimmten Rings bzw. Pads um folgende Werte multipliziert.
RING_VEL = {"yellow": 1.1,
            "magenta": 0.8,
            "red": 1.5}
PAD_VEL = {"yellow": 1.3,
           "magenta": 0.9,
           "red": 1.7}

# Der Index ist die Sternanzahl, die bei einer Completion gewonnen wird,
# und das Element ist der Name des Schwierigkeitsgrades.
DIFFICULTY = ("", "Auto", "Easy", "Normal", "Hard", "Hard",
              "Harder", "Harder", "Insane", "Insane", "Demon")

# Speicherort für das Save-File
SAVE_FILE_PATH = HOME_FOLDER + "/Documents/gdr_savefile"

# Level-Editor
EDITOR_LEVEL_MOVEMENT = LEVEL_SCROLL_SPEED * 2
EDITOR_BACKGROUND_MOVEMENT = BACKGROUND_SCROLL_SPEED * 2

# Exit Codes für Funktionen im Spiel
CONTINUE = 0
EXIT = 1
PLAY_LEVEL = 2
VIEW_SAVE_FILE = 3
OPEN_LEVEL_EDITOR = 4
SAVE_LEVEL = 5
SAVE_LEVEL_PROPERTIES = 6
NEW_LEVEL = 7

NORMAL = 10
DEATH = 11
WIN = 12
CHANGE_GRAVITY = 13

CUBE_GAMEMODE = 20
SHIP_GAMEMODE = 21
BALL_GAMEMODE = 22
