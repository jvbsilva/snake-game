import random
import pygame
from pygame.surface import Surface
import sys
from snakes.Snake import Snake, PySnake

FPS = 15
N_FOODS = 10
N_PYSNAKES = 5

SCREEN_WIDTH = 800
SCRERN_HEIGHT = 600

GRID_WIDTH = 600
GRID_HEIGHT = 600
GRID_SQUARE = 20

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

    # Create PySnakes
    pySnakes_list: list[PySnake] = []
    for _ in range(N_PYSNAKES):
        pySnakes_list.append(
            PySnake(use_available_point(available_points), GRID_SQUARE)
        )

    # Initialize PyGame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCRERN_HEIGHT))
    pygame.display.set_caption("PySnake")

    # Create grid surface
    grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
    grid_surface.fill(LIGHT_GREY)
    for x, y in GRID_WHITE:
        pygame.draw.rect(
            grid_surface, WHITE_SMOKE, pygame.Rect(x, y, GRID_SQUARE, GRID_SQUARE)
        )

    # Create grid rect for colision check
    grid_rect = pygame.Rect(0, 0, GRID_WIDTH, GRID_HEIGHT)

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

        # Check for food eaten
        if userSnake.head in food_list:
            userSnake.eat(userSnake.head.copy())
            food_list.remove(userSnake.head)
            food_list.append(use_available_point(available_points))

        # Clean the screen
        screen.fill(WHITE)

        # Blit the grid
        screen.blit(grid_surface, (0, 0))

        # Draw foods
        for food in food_list:
            pygame.draw.rect(
                screen, BLUE, pygame.Rect(food[0], food[1], GRID_SQUARE, GRID_SQUARE)
            )

        # Draw user snake
        draw_snake(screen, userSnake, RED)

        # Draw pySnakes
        for snake in pySnakes_list:
            draw_snake(screen, snake, snake.color)

        # Check for grid border colision
        if not grid_rect.collidepoint(userSnake.head[0], userSnake.head[1]):
            pygame.quit()
            sys.exit()

        # Check for self colision
        if userSnake.self_colision:
            pygame.quit()
            sys.exit()

        # Check for pySnake colision
        for snake in pySnakes_list:
            if userSnake.head in snake.body:
                pygame.quit()
                sys.exit()

        # Update the display
        pygame.display.flip()

        # Use clock to control FPS
        clock.tick(FPS)


if __name__ == "__main__":
    main()
