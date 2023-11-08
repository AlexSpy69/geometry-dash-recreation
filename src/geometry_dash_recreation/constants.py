import screeninfo

MONITOR_NR = 0

width = screeninfo.get_monitors()[MONITOR_NR].width
height = screeninfo.get_monitors()[MONITOR_NR].height

FPS = 60
DELTA_TIME = 1 / FPS
SCREEN_WIDTH = width
SCREEN_HEIGHT = height
UNIT = SCREEN_HEIGHT * 0.08
GROUND_HEIGHT = SCREEN_HEIGHT - UNIT * 3
PLAYER_POS = (UNIT * 5, GROUND_HEIGHT)
