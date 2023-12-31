import pygame
from game.scenes.game import GameScene, Text
from game.scenes.menu import MainMenuScene  

from game.settings import *


pygame.init()
pygame.display.set_caption("Tetris")

class App():

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.game_scene = GameScene(self)
        self.current_scene = self.main_menu_scene = MainMenuScene(self)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.set_timer()

    def main(self):

        while self.running:
            self.check_events()
            self.current_scene.update() 
            self.current_scene.draw(self.screen)  
            pygame.display.flip()  
            self.clock.tick(FPS)  
        pygame.quit()


    def check_events(self):
        self.anim_trigger = False
        for event in pygame.event.get():
            self.current_scene.handle_events(event) 
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == self.user_event:
                self.anim_trigger = True

    
            
    def set_timer(self):
        self.user_event = pygame.USEREVENT + 0
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pygame.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
 

    def get_opposite_scene(self):
        pygame.time.delay(250)
        if self.current_scene is self.game_scene:
            self.current_scene = self.main_menu_scene
        else:
            self.current_scene = self.game_scene

    def reinitialise_game_scene(self):
        self.game_scene = GameScene(self)


if __name__ == "__main__":
    app = App()
    app.main()
