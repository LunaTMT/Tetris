import pygame
from game import settings, colours
import random

from game.settings import *
from game.colours import *

class Block(pygame.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.game = tetromino.game

        self.pos = vec(pos) + INIT_POS_OFFSET

        super().__init__(tetromino.game.all_sprites)
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_HEIGHT])
        
        self.rect = self.image.get_rect()

    def set_rect_pos(self):
        self.rect.topleft = (self.game.tetris_x_start + (self.pos[0] * BLOCK_WIDTH), self.pos[1] * BLOCK_HEIGHT)

    def update(self):
        self.set_rect_pos()

    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < COLUMNS and y < ROWS and (
                y < 0 or not self.tetromino.game.field_array[y][x]):
            return False
        return True
    
    def handle_event(self, event):
        pass

class Tetromino:
    previous_colour = None
    def __init__(self, game):
        self.game = game
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.colour = random.choice(BLOCK_COLOURS)
        self.initialise_block_colour()

        self.landing = False
        

    def initialise_block_colour(self):
        while self.colour == self.previous_colour:
            self.colour = random.choice(BLOCK_COLOURS)
        self.previous_colour = self.colour

        for block in self.blocks:
            block.image.fill(self.colour)
    
    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == "down":
            self.landing = True

    def update(self):
        #pass
        self.move(direction="down")