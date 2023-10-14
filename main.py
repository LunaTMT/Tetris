import pygame
from game.scenes.game import GameScene
from game.scenes.menu import MainMenuScene  

from game import settings


pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

class App():

    def __init__(self) -> None:
        self.game_scene = GameScene(self)
        self.current_scene = self.main_menu_scene = MainMenuScene(self)
        self.clock = pygame.time.Clock()
        self.running = True

    def main(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.current_scene.handle_events(event)  
            self.current_scene.update() 
            self.current_scene.draw(screen)  

            pygame.display.flip()  
            self.clock.tick(settings.FPS)  
        pygame.quit()
    
    def get_opposite_scene(self):
        pygame.time.delay(250)
        if self.current_scene is self.game_scene:
            self.current_scene = self.main_menu_scene
        else:
            self.current_scene = self.game_scene

       


if __name__ == "__main__":
    app = App()
    app.main()
