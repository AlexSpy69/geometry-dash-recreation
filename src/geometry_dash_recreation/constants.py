import screeninfo

MONITOR_NR = 1

width = screeninfo.get_monitors()[MONITOR_NR].width
height = screeninfo.get_monitors()[MONITOR_NR].height

FPS = 60                        # Bilder pro Sekunde
DELTA_TIME = 60 / FPS           # Abstand zwischen zwei Frames in Sekunden multipliziert mit 60
SCREEN_WIDTH = width            # Fensterbreite
SCREEN_HEIGHT = height          # Fensterhöhe
UNIT = SCREEN_HEIGHT * 0.08     # Einheit
GROUND_HEIGHT = UNIT * 3        # Höhe des Bodens
PLAYER_POS = (UNIT * 5,
              SCREEN_HEIGHT-
              GROUND_HEIGHT)    # Ursprüngliche Position des Spielers auf dem Bildschirm
VEL_ADD = 2                     # Stärke der Einwirkung der Gravitation
JUMP_VEL = 25                   # Stärke des Sprungs des Spielers
LEVEL_SCROLL_SPEED = DELTA_TIME*2