import pygame
from pygame.surface import Surface
import sys
from snakes.Snake import Snake

SCREEN_WIDTH = 800
SCRERN_HEIGHT = 600

GRID_WIDTH = 600
GRID_HEIGHT = 600
GRID_SQUARE = 10

X_GRID = range(0, GRID_WIDTH, GRID_SQUARE)
Y_GRID = range(0, GRID_HEIGHT, GRID_SQUARE)

GRID =  [(x,y) for x in X_GRID for y in Y_GRID]
GRID_WHITE = [(x,y) for x, y in GRID if ((x  + y) / GRID_SQUARE) % 2 == 0 ]

BLACK = (0,0,0)
LIGHT_GREY = (211,211,211)
WHITE_SMOKE = (245,245,245)
WHITE = (255,255,255)
RED = (255,55,55)

def draw_snake(screen: Surface, snake: Snake, color: tuple):
    for piece in snake.body:
        pygame.draw.rect(screen, color, pygame.Rect(piece[0], piece[1], snake.square_size, snake.square_size))

def main():
    # Initialize PyGame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCRERN_HEIGHT))
    pygame.display.set_caption('PySnake')

    # Create user snake
    userSnake = Snake([300,300],GRID_SQUARE)

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    userSnake.move_left()

                if event.key == pygame.K_RIGHT:
                    userSnake.move_right()
            
                if event.key == pygame.K_UP:
                    userSnake.move_up()

                if event.key == pygame.K_DOWN:
                    userSnake.move_down()

        # Fill the screen with black color
        screen.fill(WHITE)

        # Draw the grid
        pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(0, 0, GRID_WIDTH, GRID_HEIGHT))
        for x, y in GRID_WHITE:
            pygame.draw.rect(screen, WHITE_SMOKE, pygame.Rect(x, y, GRID_SQUARE, GRID_SQUARE))

        # Draw user snake
        draw_snake(screen, userSnake, RED)

        # Update the display
        pygame.display.flip()

if __name__ == '__main__':
    main()
