import pygame
from game import colours
from game.sprites.tetromino import Tetromino
from game.settings import *

class GameScene:
    def __init__(self, app):
        self.app = app
        self.all_sprites = pygame.sprite.Group()
        self.initialise_game_borders()

        self.return_button = ReturnButton(self)
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        
        self.transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.transparent_surface.set_alpha(100)

        
        self.score = 0
        self.is_running = True

    def initialise_game_borders(self):
        self.tetris_x_start = (SCREEN_WIDTH - TETRIS_WIDTH) // 2
        self.tetris_x_end = SCREEN_WIDTH - self.tetris_x_start
        tetris_y_start = (SCREEN_HEIGHT - TETRIS_HEIGHT) // 2
        self.game_border =  pygame.Rect(self.tetris_x_start, 
                                        tetris_y_start, 
                                        TETRIS_WIDTH, TETRIS_HEIGHT)
        
    
        score_border_width = self.tetris_x_start * 0.85
        score_border_height = TETRIS_HEIGHT * 0.5
        self.score_border = pygame.Rect((self.tetris_x_start - score_border_width) // 2,
                                       (CENTER_Y - (score_border_height//2)), 
                                       score_border_width, score_border_height)
        
        hold_border_width = self.tetris_x_start * 0.85
        hold_border_height = TETRIS_HEIGHT * 0.2
        self.hold_border = pygame.Rect(self.tetris_x_end  + ((SCREEN_WIDTH - self.tetris_x_end  - hold_border_width) // 2),
                                       (SCREEN_HEIGHT * 0.10), 
                                       hold_border_width, hold_border_height)
        
        next_border_width = self.tetris_x_start * 0.85
        next_border_height = TETRIS_HEIGHT * 0.5
        self.next_border = pygame.Rect(self.tetris_x_end + ((SCREEN_WIDTH - self.tetris_x_end - next_border_width) // 2),
                                       (SCREEN_HEIGHT * 0.40), 
                                        next_border_width, next_border_height)
    
    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def get_field_array(self):
        return [[0 for c in range(COLUMNS)] for r in range(ROWS)]

    def update(self):
        
        if self.app.anim_trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetrimino_landing()
        self.all_sprites.update()
        self.check_collisions()

    def check_collisions(self):
        pass

    def check_tetrimino_landing(self):
        if self.tetromino.landing:
            self.speed_up = False
            self.put_tetromino_blocks_in_array()
            self.tetromino = Tetromino(self)
    
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
            y = i * BLOCK_HEIGHT
            pygame.draw.line(screen, colours.BACKGROUND_COLOUR, (self.tetris_x_start, y), (self.tetris_x_end, y), 1)

        # Draw vertical grid lines
        for j in range(0, COLUMNS+1):
            
            x = j * BLOCK_WIDTH
            pygame.draw.line(screen, colours.BACKGROUND_COLOUR, (self.tetris_x_start + x, 0), (self.tetris_x_start + x, TETRIS_HEIGHT), 1)

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
        self.image = self.image_normal = pygame.transform.scale(self.image_normal, (int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.1)))

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
        self.x = SCREEN_WIDTH * 0.03
        self.y = SCREEN_HEIGHT * 0.03

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