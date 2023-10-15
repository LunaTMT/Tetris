import pygame
from game import settings, colours

class Block(pygame.sprite.Sprite):
    def __init__(self, tetrimino):
        super().__init__()
        self.tetrimino = tetrimino
        self.image = pygame.Surface((32, 32)) 
        self.image.fill((255, 0, 0))  
        self.rect = self.image.get_rect()
        self.rect.center = (settings.SCREEN_WIDTH // 2, 0)  
        self.set = False

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