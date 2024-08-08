import pygame
import sys

def main():
    # Initialize PyGame
    pygame.init()

    # Set up the display
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('PySnake')

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the screen with a color (optional, for visibility)
        screen.fill((0, 0, 0))  # Black color

        # Update the display
        pygame.display.flip()

if __name__ == '__main__':
    main()
