import random
import pygame
from pygame.surface import Surface
import sys
from snakes.Snake import Snake

FPS = 60
N_FOODS = 5

SCREEN_WIDTH = 800
SCRERN_HEIGHT = 600

GRID_WIDTH = 600
GRID_HEIGHT = 600
GRID_SQUARE = 10

X_GRID = range(0, GRID_WIDTH, GRID_SQUARE)
Y_GRID = range(0, GRID_HEIGHT, GRID_SQUARE)

GRID = [(x, y) for x in X_GRID for y in Y_GRID]
GRID_WHITE = [(x, y) for x, y in GRID if ((x + y) / GRID_SQUARE) % 2 == 0]

BLACK = (0, 0, 0)
LIGHT_GREY = (211, 211, 211)
WHITE_SMOKE = (245, 245, 245)
WHITE = (255, 255, 255)
RED = (255, 55, 55)
BLUE = (55, 55, 255)


def draw_snake(screen: Surface, snake: Snake, color: tuple):
    for piece in snake.body:
        pygame.draw.rect(
            screen,
            color,
            pygame.Rect(piece[0], piece[1], snake.square_size, snake.square_size),
        )


def use_available_point(available_points: list):
    point = random.choice(available_points)
    available_points.remove(point)
    return list(point)


def main():

    # Create available_points list
    available_points = GRID.copy()

    # Create food_list
    food_list = []
    for _ in range(N_FOODS):
        food_list.append(use_available_point(available_points))

    # Create user snake
    userSnake = Snake(use_available_point(available_points), GRID_SQUARE)

    # Initialize PyGame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCRERN_HEIGHT))
    pygame.display.set_caption("PySnake")

    # Create clock to control fps
    clock = pygame.time.Clock()

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    userSnake.turn("LEFT")

                if event.key == pygame.K_RIGHT:
                    userSnake.turn("RIGHT")

                if event.key == pygame.K_UP:
                    userSnake.turn("UP")

                if event.key == pygame.K_DOWN:
                    userSnake.turn("DOWN")

        # Move user snake
        userSnake.move()

        # Clean the screen
        screen.fill(WHITE)

        # Draw the grid
        pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(0, 0, GRID_WIDTH, GRID_HEIGHT))
        for x, y in GRID_WHITE:
            pygame.draw.rect(
                screen, WHITE_SMOKE, pygame.Rect(x, y, GRID_SQUARE, GRID_SQUARE)
            )

        # Draw foods
        for food in food_list:
            pygame.draw.rect(
                screen, BLUE, pygame.Rect(food[0], food[1], GRID_SQUARE, GRID_SQUARE)
            )

        # Draw user snake
        draw_snake(screen, userSnake, RED)

        # Update the display
        pygame.display.flip()

        # Use clock to control FPS
        clock.tick(FPS)


if __name__ == "__main__":
    main()
