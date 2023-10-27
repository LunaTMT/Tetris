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
import pygame

vec = pygame.math.Vector2

BLOCK_WIDTH = TETRIS_WIDTH // 10
BLOCK_HEIGHT = TETRIS_HEIGHT // 20

CENTER_X = SCREEN_WIDTH//2
CENTER_Y = SCREEN_HEIGHT//2
FPS = 60

 
FIELD_SIZE = ROWS, COLUMNS = 20, 10

BACKGROUND_COLOUR = (0,119,182)

INIT_POS_OFFSET = vec(COLUMNS // 2 - 1, 0)
NEXT_POS_OFFSET = vec(COLUMNS * 1.2, ROWS * 0.77)
HOLD_POS_OFFSET = vec(COLUMNS * 1.2, ROWS * 0.25)

ANIM_TIME_INTERVAL = 150  # milliseconds
FAST_ANIM_TIME_INTERVAL = 15

MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

TETROMINOES = {
    'T': [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z': [(0, 0), (1, 0), (0, -1), (-1, -1)]
}

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

   