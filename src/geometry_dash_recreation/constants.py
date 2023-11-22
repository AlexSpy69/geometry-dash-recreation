import screeninfo

MONITOR_NR = 1

width = screeninfo.get_monitors()[MONITOR_NR].width
height = screeninfo.get_monitors()[MONITOR_NR].height

FPS = 60                        # Bilder pro Sekunde
DELTA_TIME = 60 / FPS           # Abstand zwischen zwei Frames in Sekunden multipliziert mit 60
SCREEN_WIDTH = width            # Fensterbreite
SCREEN_HEIGHT = height          # Fensterhöhe
UNIT = SCREEN_HEIGHT * 0.08     # Einheit
GROUND_HEIGHT = UNIT * 10        # Höhe des Bodens
PLAYER_POS = (UNIT * 5,
              GROUND_HEIGHT)    # Ursprüngliche Position des Spielers auf dem Bildschirm
VEL_ADD = 2                     # Stärke der Einwirkung der Gravitation
JUMP_VEL = 25                   # Stärke des Sprungs des Spielers
LEVEL_SCROLL_SPEED = DELTA_TIME*6  # Die Geschwindigkeit, mit der die Objekte in einem Level nach links scrollen
START_LEVEL = "levels/start"    # Das Level, mit dem das Spiel automatisch beginnt
DEATH_ACCURACY = 20 / DELTA_TIME
