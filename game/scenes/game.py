import pygame
from game import colours
from game.sprites.tetromino import Tetromino
from game.settings import *
from game import settings
import pygame.freetype as ft 

class Text:
    def __init__(self, app) -> None:
        self.app = app
        self.font = ft.Font("assets/fonts/Title.ttf")
    
    def draw(self):
        self.font.render_to(self.app.screen, (settings.SCREEN_WIDTH* 0.815, settings.SCREEN_HEIGHT*0.03), 
                            text="Hold", fgcolor='white', size=settings.SCREEN_WIDTH * 0.05)
        
        self.font.render_to(self.app.screen, (settings.SCREEN_WIDTH* 0.815, settings.SCREEN_HEIGHT*0.53), 
                            text="Next", fgcolor='white', size=settings.SCREEN_WIDTH * 0.05)
        
        self.font.render_to(self.app.screen, (settings.SCREEN_WIDTH* 0.05, settings.SCREEN_HEIGHT*0.18), 
                            text="Score", fgcolor='white', size=settings.SCREEN_WIDTH * 0.05)


        

class GameScene:
    def __init__(self, app):
        self.app = app
        self.all_sprites = pygame.sprite.Group()
        self.initialise_game_borders()

        self.return_button = ReturnButton(self)
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.text = Text(self.app)

        self.transparent_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.transparent_surface.set_alpha(100)

        
        self.score = 0
        self.is_running = True

    def initialise_game_borders(self):

        self.tetris_x_start = (settings.SCREEN_WIDTH - settings.TETRIS_WIDTH) // 2
        self.tetris_x_end = settings.SCREEN_WIDTH - self.tetris_x_start
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
        hold_border_height = settings.TETRIS_HEIGHT * 0.35
        self.hold_border = pygame.Rect(self.tetris_x_end  + ((settings.SCREEN_WIDTH - self.tetris_x_end  - hold_border_width) // 2),
                                       (settings.SCREEN_HEIGHT * 0.10), 
                                       hold_border_width, hold_border_height)
        
        next_border_width = self.tetris_x_start * 0.85
        next_border_height = settings.TETRIS_HEIGHT * 0.35
        self.next_border = pygame.Rect(self.tetris_x_end + ((settings.SCREEN_WIDTH - self.tetris_x_end - next_border_width) // 2),
                                       (settings.SCREEN_HEIGHT * 0.6), 
                                        next_border_width, next_border_height)
    
    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for c in range(settings.COLUMNS)] for r in range(settings.ROWS)]

    def update(self):
        if self.app.anim_trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetrimino_landing()
        self.all_sprites.update()
        self.check_collisions()

    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == settings.INIT_POS_OFFSET[1]:
            pygame.time.wait(300)
            return True

    def check_collisions(self):
        pass

    def check_tetrimino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def check_full_lines(self):
        row = ROWS - 1
        for r in range(ROWS-1, -1, -1):
            for c in range(COLUMNS):
                self.field_array[row][c] = self.field_array[r][c]

                if self.field_array[r][c]:
                    self.field_array[row][c].pos = vec(c, r)
            
            if sum(map(bool, self.field_array[r])) < COLUMNS:
                row -= 1
            else:
                for c in range(COLUMNS):
                    self.field_array[row][c].alive = False
                    self.field_array[row][c] = 0

    def handle_events(self, event):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.tetromino.move(direction='left')
        elif keys[pygame.K_RIGHT]:
            self.tetromino.move(direction='right')
        elif keys[pygame.K_DOWN]:
            self.tetromino.move(direction='down')
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.tetromino.rotate()
        
        self.return_button.handle_event(event)


    def draw(self, screen):
        
        screen.fill(colours.BACKGROUND_COLOUR)
        screen.blit(self.transparent_surface, (0, 0))
        
        self.draw_borders(screen)
        self.draw_grid(screen)
        self.draw_score(screen)
   
        self.return_button.draw(screen)
        self.all_sprites.draw(screen) 

        self.text.draw()
   


        
        
    def draw_borders(self, screen):
        pygame.draw.rect(screen, colours.BLACK, self.game_border)
        pygame.draw.rect(screen, colours.BLACK, self.hold_border, border_radius=8)
        pygame.draw.rect(screen, colours.BLACK, self.score_border, border_radius=8)
        pygame.draw.rect(screen, colours.BLACK, self.next_border, border_radius=8)
  

    def draw_score(self, screen):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, colours.WHITE)
        #screen.blit(score_text, (10, 10))

    def draw_grid(self, screen):
        # (self.tetris_x_start, y), (self.tetris_x_end, y)
        #Diagonal Lines
        for i in range(1, ROWS):
            y = i * settings.BLOCK_HEIGHT
            pygame.draw.line(screen, colours.BACKGROUND_COLOUR, (self.tetris_x_start, y), (self.tetris_x_end, y), 1)

        # Draw vertical grid lines
        for j in range(0, COLUMNS+1):
            
            x = j * settings.BLOCK_WIDTH
            pygame.draw.line(screen, colours.BACKGROUND_COLOUR, (self.tetris_x_start + x, 0), (self.tetris_x_start + x, settings.TETRIS_HEIGHT), 1)

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