"""Dieses Modul enthält Konstanten mit wichtigen Einstellungen, an denen sich das gesamte Programm richtet,
wie z. B. die Fenstergröße, die Seitenlänge eines einzelnen Spielblocks oder die Höhe, mit der der Spieler springt.
Diese können bei Bedarf vom Benutzer eingestellt oder angepasst werden."""

import screeninfo
from pathlib import Path
import pkg_resources
import sys
from geometry_dash_recreation import util


def adapt_res(w: int, h: int) -> tuple:
    """
    Liefert ein Tupel mit einer für den Fullscreen-Modus angepassten Bildschirmgröße.

    :param w: Bildschirmweite
    :param h: Bildschirmhöhe

    :returns: w, w * 9/16
    """

    if w/h != 16/9:
        w = int(w * 9/16)
    return w, h


FULLSCREEN = None
MONITOR_NR = None

try:
    width, height = map(int, sys.argv[1:3])
    FULLSCREEN = False
    MONITOR_NR = -1
except (ValueError, IndexError):
    try:
        MONITOR_NR = int(sys.argv[1])
        width = screeninfo.get_monitors()[MONITOR_NR].width
        height = screeninfo.get_monitors()[MONITOR_NR].height
        width, height = adapt_res(width, height)
        FULLSCREEN = True
    except (ValueError, IndexError):
        width, height = 640, 360
        FULLSCREEN = False
        MONITOR_NR = -1


# Home-Ordner
HOME_FOLDER = str(Path.home())

# Ressourcen-Ordner
ASSETS_FOLDER = pkg_resources.resource_filename("geometry_dash_recreation", "assets")
MAIN_LEVELS_FOLDER = pkg_resources.resource_filename("geometry_dash_recreation", "main_levels_folder")
USER_LEVELS_FOLDER = pkg_resources.resource_filename("geometry_dash_recreation", "user_levels_folder")

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
DEATH_ACCURACY = UNIT / 4
OUT_OF_BOUNDS = -6000
ATTEMPT_COUNT_POS = (SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.4)

# Mögliche Level-Komponenten-Eigenschaften
COMPONENT_IMGFILE_LIST = tuple(sorted(util.list_files(ASSETS_FOLDER + "/textures/components", ".png")))
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

# level.level_select.loop()
CONTINUE = 0                # Der Loop fährt normal fort.
EXIT = 1                    # Das Spiel soll beendet werden.
PLAY_LEVEL = 2              # Das gerade ausgewählte Level soll gespielt werden.
VIEW_SAVE_FILE = 3          # Der Save-File-Viewer soll geöffnet werden.
OPEN_LEVEL_EDITOR = 4       # Der Level-Editor soll geöffnet werden.
SAVE_LEVEL = 5              # Das Level soll gespeichert werden.
SAVE_LEVEL_PROPERTIES = 6   # Die Level-Eigenschaften sollen gespeichert werden.
NEW_LEVEL = 7               # Es soll ein neues Level erzeugt werden.

# game_sprites.Gamemode().controls()
NORMAL = 10                 # Das Spiel fährt normal fort.
DEATH = 11                  # Der Spieler soll getötet werden.
WIN = 12                    # Der Spieler hat das Ende des Levels erreicht.
CHANGE_GRAVITY = 13         # Die Grawitationsrichtung soll gewechselt werden.

CUBE_GAMEMODE = 20          # Das Spiel soll zum Cube-Gamemode wechseln.
SHIP_GAMEMODE = 21          # Das Spiel soll zum Ship-Gamemode wechseln.
BALL_GAMEMODE = 22          # Das Spiel soll zum Ball-Gamemode wechseln.


def create_all_list() -> list:
    all_vars = list(globals().keys())
    to_remove = "screeninfo", "Path", "pkg_resources", "sys", "util", "width", "height", "adapt_res", "create_all_list"
    for to_remove_element in to_remove:
        all_vars.remove(to_remove_element)

    return all_vars


__all__ = create_all_list()
