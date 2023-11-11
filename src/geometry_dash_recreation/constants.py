import screeninfo

MONITOR_NR = 1

width = screeninfo.get_monitors()[MONITOR_NR].width
height = screeninfo.get_monitors()[MONITOR_NR].height

FPS = 60
DELTA_TIME = 60 / FPS
SCREEN_WIDTH = width
SCREEN_HEIGHT = height
UNIT = SCREEN_HEIGHT * 0.08
GROUND_HEIGHT = UNIT * 3
PLAYER_POS = (UNIT * 5, SCREEN_HEIGHT-GROUND_HEIGHT)
VEL_ADD = 2
JUMP_VEL = 25
