import screeninfo

MONITOR_NR = 0

width = screeninfo.get_monitors()[MONITOR_NR].width
height = screeninfo.get_monitors()[MONITOR_NR].height

FPS = 30                        # Bilder pro Sekunde
DELTA_TIME = 60 / FPS           # Abstand zwischen zwei Frames in Sekunden multipliziert mit 60
SCREEN_WIDTH = 1600            # Fensterbreite
SCREEN_HEIGHT = 900          # Fensterhöhe
RESIZE = SCREEN_HEIGHT/1080
UNIT = SCREEN_HEIGHT * 0.08     # Einheit
GROUND_HEIGHT = UNIT * 10       # Höhe des Bodens
CEILING_HEIGHT = UNIT * 1       # Höhe der Decke
CEILING_MOVE = CEILING_HEIGHT/5
PLAYER_POS = (UNIT * 5,
              GROUND_HEIGHT)    # Ursprüngliche Position des Spielers auf dem Bildschirm
VEL_ADD = 2                     # Stärke der Einwirkung der Gravitation
JUMP_VEL = 27                   # Stärke des Sprungs des Spielers
LEVEL_SCROLL_SPEED = DELTA_TIME*14*RESIZE  # Die Geschwindigkeit, mit der die Objekte in einem Level nach links scrollen
BACKGROUND_SCROLL_SPEED = DELTA_TIME*3*RESIZE # Die Geschwindigkeit, mit der der Hintergrund nach links scrollt
START_LEVEL = "levels/start"    # Das Level, mit dem das Spiel automatisch beginnt
DEATH_ACCURACY = 20
RING_VEL = {"yellow": 1.1,
            "magenta": 0.8,
            "red": 1.5}
PAD_VEL = {"yellow": 1.3,
           "magenta": 0.9,
           "red": 1.7}

# Exit Codes
NORMAL = 0
DEATH = 1
WIN = 2
CHANGE_GRAVITY = 3

CUBE_GAMEMODE = 10
SHIP_GAMEMODE = 11
BALL_GAMEMODE = 12