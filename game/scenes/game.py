import pygame
from game import settings, colours

class GameScene:
    def __init__(self, app):
        self.app = app
        self.all_sprites = pygame.sprite.Group()
        self.initialise_game_borders()

        self.return_button = ReturnButton(self)
        self.score = 0
        self.is_running = True

    def initialise_game_borders(self):
        self.tetris_x_start = (settings.SCREEN_WIDTH - settings.TETRIS_WIDTH) // 2
        tetris_x_end = settings.SCREEN_WIDTH - self.tetris_x_start
        tetris_y_start = (settings.SCREEN_HEIGHT - settings.TETRIS_HEIGHT) // 2
        self.game_border =  pygame.Rect(self.tetris_x_start, 
                                        tetris_y_start, 
                                        settings.TETRIS_WIDTH, settings.TETRIS_HEIGHT)
    
        
        score_border_width = self.tetris_x_start * 0.85
        score_border_height = settings.TETRIS_HEIGHT * 0.5
        self.score_border = pygame.Rect((self.tetris_x_start - score_border_width) // 2,
                                       (settings.CENTER_Y - (score_border_height//2)), 
                                       score_border_width, score_border_height)
        
        hold_border_width = self.tetris_x_start * 0.85
        hold_border_height = settings.TETRIS_HEIGHT * 0.2
        self.hold_border = pygame.Rect(tetris_x_end + ((settings.SCREEN_WIDTH - tetris_x_end - hold_border_width) // 2),
                                       (settings.SCREEN_HEIGHT * 0.10), 
                                       hold_border_width, hold_border_height)
        
        next_border_width = self.tetris_x_start * 0.85
        next_border_height = settings.TETRIS_HEIGHT * 0.5
        self.next_border = pygame.Rect(tetris_x_end + ((settings.SCREEN_WIDTH - tetris_x_end - next_border_width) // 2),
                                       (settings.SCREEN_HEIGHT * 0.40), 
                                        next_border_width, next_border_height)


    def update(self):
        self.all_sprites.update()
        self.check_collisions()

    def check_collisions(self):
        pass
        """collisions = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if collisions:
            self.player.handle_collision()
            self.score += 1"""
    
    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False

        self.return_button.handle_event(event)


    def draw(self, screen):
        screen.fill(colours.BACKGROUND_COLOUR)
        pygame.draw.rect(screen, colours.BLACK, self.game_border, border_radius=8)
        pygame.draw.rect(screen, colours.BLACK, self.hold_border, border_radius=8)
        pygame.draw.rect(screen, colours.BLACK, self.score_border, border_radius=8)
        pygame.draw.rect(screen, colours.BLACK, self.next_border, border_radius=8)
        
        self.return_button.draw(screen)
        
        self.all_sprites.draw(screen) 
        self.draw_score(screen)

    def draw_score(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, colours.WHITE)
        #screen.blit(score_text, (10, 10))

    def should_switch_to_menu(self):
        pass

    def should_quit_game(self):
        pass

class ReturnButton:
    def __init__(self, game):
        self.game = game
        self.app = game.app
        
        self.initialise_position()

        self.image_normal = pygame.image.load('assets/images/return.png')
        self.image = self.image_normal = pygame.transform.scale(self.image_normal, (int(settings.SCREEN_WIDTH * 0.1), int(settings.SCREEN_HEIGHT * 0.1)))

        original_width, original_height = self.image_normal.get_size()
        enlarged_image = pygame.transform.scale(self.image_normal, (int(original_width * 1.05), int(original_height * 1.05)))
        self.image_hover = enlarged_image
        self.image_clicked = self.image_normal

        self.rect = self.image.get_rect()
        self.x = (self.game.tetris_x_start - original_width) // 2
        self.rect.topleft = (self.x, self.y)

        self.sound = pygame.mixer.Sound('assets/sounds/return.wav')
        self.sound.set_volume(self.sound.get_volume() * 2)
        
    def initialise_position(self):
        self.x = settings.SCREEN_WIDTH * 0.03
        self.y = settings.SCREEN_HEIGHT * 0.03

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_hover
                self.rect.width, self.rect.height = self.image.get_size()
            else:
                self.image = self.image_normal
                self.rect.width, self.rect.height = self.image.get_size()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_clicked
                self.rect.width, self.rect.height = self.image.get_size()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_hover
                self.rect.width, self.rect.height = self.image.get_size()
                
                self.app.get_opposite_scene()
                self.sound.play()
  
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)      