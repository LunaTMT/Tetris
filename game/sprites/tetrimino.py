import pygame
from game import settings, colours

class Block(pygame.sprite.Sprite):
    def __init__(self, tetrimino, pos):
        self.tetrimino = tetrimino

        super().__init__(tetrimino.game.sprite_group)
        self.image = pygame.surface([settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT])
        self.image.fill('orange')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos[0] * settings.BLOCK_WIDTH, pos[0] * settings.BLOCK_WIDTH

    def update(self):
        pass

    def handle_event(self, event):
        if not self.set and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                print("Arrow Down key pressed")
            elif event.key == pygame.K_LEFT:
                print("Arrow Left key pressed")
            elif event.key == pygame.K_RIGHT:
            
                print("Arrow Right key pressed")

class Tetrimino:
    def __init__(self, game):
        self.game = game
        Block(self, (4, 7))

    def update(self):
        pass