import pygame
from game import settings, colours
import random

from game.settings import *
from game.colours import *

class Block(pygame.sprite.Sprite):
    def __init__(self, tetromino, pos, colour):
        self.tetromino = tetromino
        self.game = tetromino.game
        self.colour = colour
        self.alive = True
        self.default_pos = pos
        self.pos = vec(pos) + settings.INIT_POS_OFFSET
        self.next_pos = vec(pos) + settings.NEXT_POS_OFFSET
        self.hold_pos = vec(pos) + settings.HOLD_POS_OFFSET

        super().__init__(tetromino.game.all_sprites)
        self.image = pygame.Surface([settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT])
        pygame.draw.rect(self.image, colour, (1, 1, settings.BLOCK_WIDTH-1, settings.BLOCK_HEIGHT-1), border_radius=2)
        self.rect = self.image.get_rect()

    def set_rect_pos(self):
        if self.tetromino.current:
            pos = self.pos
        else:
            pos = self.next_pos
        
        if self.tetromino.hold:
            pos = self.hold_pos

        self.rect.topleft = (self.game.tetris_x_start + (pos[0] * settings.BLOCK_WIDTH), pos[1] * settings.BLOCK_HEIGHT)
        
    def update(self):
        
        self.is_alive()
        self.set_rect_pos()

    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos


    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < COLUMNS and y < ROWS and (
                y < 0 or not self.tetromino.game.field_array[y][x]):
            return False
        return True
    
    def is_alive(self):
        if not self.alive:
            self.kill()

    def handle_event(self, event):
        pass

class Tetromino:
    previous_colour = None
    def __init__(self, game, current=True, hold=False):
        self.game = game
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.initialise_block_colour()
        self.blocks = [Block(self, pos, self.colour) for pos in TETROMINOES[self.shape]]
        self.current = current
        self.landing = False
        self.hold = False
        

    def initialise_block_colour(self):
        self.colour = random.choice(BLOCK_COLOURS)
        while self.colour == self.previous_colour:
            self.colour = random.choice(BLOCK_COLOURS)
        self.previous_colour = self.colour

    def set_default_position(self):
        for block in self.blocks:
            block.pos = block.default_pos + settings.INIT_POS_OFFSET
    
    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))

    def rotate(self):
        if self.shape != "O":
            pivot_pos = self.blocks[0].pos
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            if not self.is_collide(new_block_positions):
                for i, block in enumerate(self.blocks):
                    block.pos = new_block_positions[i]

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
        self.move(direction="down")
        self.game.score += 1