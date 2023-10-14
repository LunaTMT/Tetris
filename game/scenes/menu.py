import pygame
from game import settings, colours

pygame.mixer.init()  

class MainMenuScene:
    def __init__(self, app):
        # Initialize fonts, menu options, selected option index, and color settings
        self.app = app
        self.text_color = (255, 255, 255)
        self.highlighted_color = (255, 255, 0)  # Change this to the desired highlighted color

        self.initialise_fonts()
        self.initialise_buttons()
        
    
        self.is_running = True
        self.options_menu = False
        self.option_chose = None

    def initialise_fonts(self):
        self.title_font = pygame.font.Font("assets/fonts/Title.ttf", int(settings.SCREEN_WIDTH * 0.1))
        self.menu_font = pygame.font.Font(None, int(settings.SCREEN_WIDTH * 0.3))
    
    def initialise_buttons(self):
        """
        Main Menu Buttons
        """
        button_width = int(settings.SCREEN_WIDTH * 0.3)
        button_height = int(settings.SCREEN_HEIGHT * 0.1)

        self.start_game_button = MenuButton(self, 
                                        None, settings.SCREEN_HEIGHT * 0.3, 
                                        button_width, button_height, "Start Game")
        self.options_button = MenuButton(self, 
                                     None, settings.SCREEN_HEIGHT * 0.5, 
                                     button_width, button_height, "Options")
        self.quit_button = MenuButton(self, 
                                  None, settings.SCREEN_HEIGHT * 0.7, 
                                  button_width, button_height, "Quit")
        """
        Option buttons for screen size change
        """
        self.large_button = OptionButton(self, 
                                        None, settings.SCREEN_HEIGHT * 0.3, 
                                        button_width, button_height, "Large")
        self.medium_button = OptionButton(self, 
                                        None, settings.SCREEN_HEIGHT * 0.5, 
                                        button_width, button_height, "Medium")
        self.small_button = OptionButton(self, 
                                        None, settings.SCREEN_HEIGHT * 0.7, 
                                        button_width, button_height, "Small")
        """
        Return from options back to main menu 
        """
        self.return_button = ReturnButton(self)
        

        self.buttons = self.main_menu_buttons = [self.start_game_button, self.options_button, self.quit_button]
        self.option_buttons = [self.large_button, self.medium_button, self.small_button]
        
    
    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.is_running = False

        for button in self.buttons:
            button.handle_event(event)
        
        if self.options_menu:
            self.return_button.handle_event(event)

    def update(self):
        self.check_selected()
        

    def draw(self, screen):
        screen.fill(colours.BACKGROUND_COLOUR)  # Clear the screen
        title_text = self.title_font.render("Tetris", True, colours.WHITE)
        screen.blit(title_text, (settings.SCREEN_WIDTH // 2 - title_text.get_width() // 2, settings.SCREEN_HEIGHT * 0.1))

        for button in self.buttons:
            button.draw(screen)

        if self.options_menu:
            self.return_button.draw(screen)

    def check_selected(self):
        match self.option_chose:
            case "Start Game":
                self.option_chose = None
                self.app.get_opposite_scene()
            case "Options":
                self.show_options()
            case "Quit":
                self.quit_game()


    def show_options(self):
        print("showing Options")
        self.options_menu = True
        self.buttons = self.option_buttons
        pass

    def quit_game(self):
        pygame.time.delay(500)
        pygame.quit()

class MenuButton:
    CLICK = pygame.mixer.Sound('assets/sounds/click.wav')
    DEFAULT_COLOUR = (40, 75, 100)
    HOVER_COLOUR = (9, 48, 80)

    def __init__(self, menu, x, y, width, height, text):
        self.menu = menu
        self.app = menu.app

        x = (settings.SCREEN_WIDTH - width) // 2
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colour = self.DEFAULT_COLOUR
        self.is_hovered = False
        self.name = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=8)
        text_surface = pygame.font.Font(None, 36).render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            self.colour = self.HOVER_COLOUR if self.is_hovered else self.DEFAULT_COLOUR
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            self.on_click()

    def on_click(self):
        self.CLICK.play()
        self.menu.option_chose = self.name

class OptionButton(MenuButton):
    def on_click(self):
        self.CLICK.play()
        match self.text:
            case "Large":
                settings.set_screen(1000, 800)
            case "Medium":
                settings.set_screen(900, 700)
            case "Small":
                settings.set_screen(800, 600)  
        settings.update_variables()
        pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.menu.initialise_fonts()
        self.menu.initialise_buttons()
        self.menu.return_button.initialise_position()
        self.app.game_scene.initialise_game_borders()

class ReturnButton:
    def __init__(self, menu):
        self.menu = menu
        self.app = menu.app

        self.initialise_position()

        self.image_normal = pygame.image.load('assets/images/return.png')
        self.image = self.image_normal = pygame.transform.scale(self.image_normal, (int(settings.SCREEN_WIDTH * 0.1), int(settings.SCREEN_HEIGHT * 0.1)))

        original_width, original_height = self.image_normal.get_size()
        enlarged_image = pygame.transform.scale(self.image_normal, (int(original_width * 1.05), int(original_height * 1.05)))
        self.image_hover = enlarged_image
        self.image_clicked = self.image_normal

        self.rect = self.image.get_rect()
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
                
                self.menu.buttons = self.menu.main_menu_buttons
                self.menu.options_menu = False
                self.menu.option_chose = None
                self.sound.play()
  

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)       

