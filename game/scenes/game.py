import pygame
from game import colours
from game.sprites.tetromino import Tetromino
from game.settings import *
from game.colours import *
from game import settings
import pygame.freetype as ft 

class Text:
    def __init__(self, app, game) -> None:
        self.app = app
        self.game = game
        
        self.font_size = int(settings.SCREEN_WIDTH * 0.05)
        self.font = pygame.font.Font("assets/fonts/Title.ttf", self.font_size)  # You can replace "None" with a specific font file

        """ TITLES """
        """ -------"""
        self.score = self.font.render("Score", True, WHITE) 
        self.score_board_center_x = (game.score_border_x + (game.score_border_width/2))
        
        self.score_x = self.score_board_center_x - (self.score.get_width()//2)
        self.score_y = (self.game.score_border_y - self.score.get_height()) 

        self.points = self.font.render("Points", True, WHITE) 
        self.points_x = (game.score_border_x + (game.score_border_width/2)) - (self.points.get_width()//2)
        self.lines = self.font.render("Lines", True, WHITE) 
        self.lines_x = (game.score_border_x + (game.score_border_width/2)) - (self.lines.get_width()//2)
        
        self.hold =  self.font.render("Hold", True, WHITE) 
        self.hold_x =  (game.hold_border_x + (game.hold_border_width/2)) - (self.hold.get_width()//2)
        self.hold_y = (self.game.hold_border_y - self.hold.get_height()) 
        
        
        self.next =  self.font.render("Next", True, WHITE) 
        self.next_x = (game.next_border_x + (game.next_border_width/2)) - (self.next.get_width()//2)
        self.next_y = (self.game.next_border_y - self.next.get_height()) 
        """ ------- """
    
    
    def draw(self):
        self.app.screen.blit(self.score, (self.score_x, self.score_y))
        self.app.screen.blit(self.hold, (self.hold_x, self.hold_y))
        self.app.screen.blit(self.next, (self.next_x, self.next_y))
        self.app.screen.blit(self.points, (self.points_x, self.score_y * 1.7))
        self.app.screen.blit(self.lines, (self.lines_x, self.score_y * 3))

        self.game_score = self.font.render(str(self.game.score), True, WHITE) 
        self.game_score_x = self.score_board_center_x - (self.game_score.get_width()//2)
        self.game_score_y = (self.game.score_border_y + (self.game.score_border_height/2)) - (self.game_score.get_height()//2)
        self.app.screen.blit(self.game_score, (self.game_score_x, self.game_score_y * 0.8))

        self.line_score = self.font.render(str(self.game.lines), True, WHITE) 
        self.line_score_x = self.score_board_center_x - (self.line_score.get_width()//2)
        self.line_score_y = (self.game.score_border_y + (self.game.score_border_height/2)) - (self.line_score.get_height()//2)
        self.app.screen.blit(self.line_score, (self.line_score_x, self.line_score_y * 1.3))

        

class GameScene:
    def __init__(self, app):
        self.app = app
        self.all_sprites = pygame.sprite.Group()
        self.initialise_game_borders()

        self.return_button = ReturnButton(self)
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.hold_tetromino = None
        self.text = Text(self.app, self)

        self.transparent_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.transparent_surface.set_alpha(100)

        self.score = 0
        self.lines = 0
        self.is_running = True

    def initialise_game_borders(self):

        self.tetris_x_start = (settings.SCREEN_WIDTH - settings.TETRIS_WIDTH) // 2
        self.tetris_x_end = settings.SCREEN_WIDTH - self.tetris_x_start
        tetris_y_start = (settings.SCREEN_HEIGHT - settings.TETRIS_HEIGHT) // 2
        self.game_border =  pygame.Rect(self.tetris_x_start, 
                                        tetris_y_start, 
                                        settings.TETRIS_WIDTH, settings.TETRIS_HEIGHT)
        
    
        self.score_border_width = self.tetris_x_start * 0.85
        self.score_border_height = settings.TETRIS_HEIGHT * 0.5
        self.score_border_x = (self.tetris_x_start - self.score_border_width) // 2
        self.score_border_y = (settings.CENTER_Y - (self.score_border_height//2))
        self.score_border = pygame.Rect(self.score_border_x,
                                       self.score_border_y, 
                                       self.score_border_width, self.score_border_height)
        
        self.hold_border_width = self.tetris_x_start * 0.85
        self.hold_border_height = settings.TETRIS_HEIGHT * 0.35
        self.hold_border_x = self.tetris_x_end  + ((settings.SCREEN_WIDTH - self.tetris_x_end  - self.hold_border_width) // 2)
        self.hold_border_y = (settings.SCREEN_HEIGHT * 0.10)
        self.hold_border = pygame.Rect(self.hold_border_x,
                                       self.hold_border_y, 
                                       self.hold_border_width, self.hold_border_height)
        
        self.next_border_width = self.tetris_x_start * 0.85
        self.next_border_height = settings.TETRIS_HEIGHT * 0.35
        self.next_border_x = self.tetris_x_end + ((settings.SCREEN_WIDTH - self.tetris_x_end - self.next_border_width) // 2)
        self.next_border_y = (settings.SCREEN_HEIGHT * 0.6)
        self.next_border = pygame.Rect(self.next_border_x,
                                       self.next_border_y, 
                                       self.next_border_width, self.next_border_height)
    
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
                self.lines += 1
                for c in range(COLUMNS):
                    self.score += 10
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
            self.score += 1



        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.tetromino.rotate()
            elif event.key == pygame.K_h:
                if self.hold_tetromino:
                    self.tetromino, self.hold_tetromino = self.hold_tetromino, self.tetromino
                    self.hold_tetromino.hold = True
                    self.tetromino.hold = False
                else:
                    self.hold_tetromino = self.tetromino
                    self.hold_tetromino.hold = True

                    self.tetromino = self.next_tetromino
                    self.tetromino.current = True
                    self.next_tetromino = Tetromino(self, current=False)
                
                self.tetromino.set_default_position()

        
        
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