import pygame

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Translucent Line")

# Create a transparent surface
transparent_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

# Set the alpha (transparency) value for the surface
alpha_value = 50  # Adjust as needed (0 to 255)
transparent_surface.set_alpha(alpha_value)

# Define line color (fully opaque)
line_color = (255, 0, 0)  # Red

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw a line with the specified color on the transparent surface
    pygame.draw.line(transparent_surface, line_color, (100, 100), (540, 380), 5)  # The "5" is the line thickness

    # Blit the transparent surface onto the screen
    screen.blit(transparent_surface, (0, 0))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
