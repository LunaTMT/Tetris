import pygame
# Large - 1000 X 800
# Medium - 900 X 700
# Small - 800 X 600


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

TETRIS_WIDTH = SCREEN_HEIGHT - 200
TETRIS_HEIGHT = SCREEN_WIDTH - 200

"""
Number of blocks for width 10
number of blocks for height 20
"""

BLOCK_WIDTH = TETRIS_WIDTH / 10
BLOCK_HEIGHT = TETRIS_HEIGHT / 20

CENTER_X = SCREEN_WIDTH//2
CENTER_Y = SCREEN_HEIGHT//2
FPS = 60

BACKGROUND_COLOUR = (0,119,182)





def update_variables():
    global TETRIS_WIDTH
    global TETRIS_HEIGHT
    global BLOCK_WIDTH
    global BLOCK_HEIGHT
    global CENTER_X
    global CENTER_Y

    TETRIS_WIDTH = SCREEN_HEIGHT - 200
    TETRIS_HEIGHT = SCREEN_WIDTH - 200

    BLOCK_WIDTH = TETRIS_WIDTH / 10
    BLOCK_HEIGHT = TETRIS_HEIGHT / 20

    CENTER_X = SCREEN_WIDTH//2
    CENTER_Y = SCREEN_HEIGHT//2

def set_screen(width, height):
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height

   