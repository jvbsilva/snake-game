import random
import pygame
from pygame.surface import Surface
import sys
from snakes.Snake import Snake, UserSnake, PySnake

FPS = 5
N_FOODS = 25
N_PYSNAKES = 1

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
ORANGE = (255, 165, 0)
BLUE = (55, 55, 255)
GREEN = (0, 225, 0)
DARK_GREEN = (0, 125, 0)


def create_rect_with_border(width, height, inner_color, border_color, border_size):
    # Create a surface with the desired dimensions including borders
    surface = pygame.Surface((width, height))

    # Fill the entire surface with the border color
    surface.fill(border_color)

    # Draw the inner rectangle (leaving space for the border)
    inner_rect = pygame.Rect(
        border_size, border_size, width - 2 * border_size, height - 2 * border_size
    )
    pygame.draw.rect(surface, inner_color, inner_rect)

    return surface


user_snake_body_rect = create_rect_with_border(GRID_SQUARE, GRID_SQUARE, RED, BLACK, 2)
user_snake_head_rect = create_rect_with_border(
    GRID_SQUARE, GRID_SQUARE, ORANGE, BLACK, 2
)

pySnake_body_rect = create_rect_with_border(GRID_SQUARE, GRID_SQUARE, GREEN, BLACK, 2)
pySnake_head_rect = create_rect_with_border(
    GRID_SQUARE, GRID_SQUARE, DARK_GREEN, BLACK, 2
)

food_rect = create_rect_with_border(GRID_SQUARE, GRID_SQUARE, BLUE, BLACK, 2)


def draw_snake(screen: Surface, snake: Snake, body_surf: Surface, head_surf: Surface):
    for piece in snake.body:
        screen.blit(body_surf, (piece[0], piece[1]))
    screen.blit(head_surf, (snake.head[0], snake.head[1]))


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
    userSnake = UserSnake(use_available_point(available_points), GRID_SQUARE)

    # Create PySnakes
    pySnakes_list: list[PySnake] = []
    for _ in range(N_PYSNAKES):
        pySnakes_list.append(
            PySnake(use_available_point(available_points), GRID_SQUARE)
        )

    # Chose target food for PySnakes
    for snake in pySnakes_list:
        snake.chose_target_food(food_list)

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

        # Move snakes
        userSnake.move()

        for snake in pySnakes_list:
            snake.chase_food()
            snake.move()

        # Check for food eaten
        was_food_eaten = False
        if userSnake.head in food_list:
            userSnake.eat(userSnake.head.copy())
            food_list.remove(userSnake.head)
            food_list.append(use_available_point(available_points))
            was_food_eaten = True

        for snake in pySnakes_list:
            if snake.head in food_list:
                snake.eat(snake.head.copy())
                food_list.remove(snake.head)
                food_list.append(use_available_point(available_points))
                was_food_eaten = True

        if was_food_eaten:
            for snake in pySnakes_list:
                snake.chose_target_food(food_list)

        # Clean the screen
        screen.fill(WHITE)

        # Blit the grid
        screen.blit(grid_surface, (0, 0))

        # Draw foods
        for food in food_list:
            screen.blit(food_rect, (food[0], food[1]))

        # Draw user snake
        # draw_snake(screen, userSnake, user_snake_body_rect, user_snake_head_rect)

        # Draw pySnakes
        for snake in pySnakes_list:
            draw_snake(screen, snake, pySnake_body_rect, pySnake_head_rect)
            screen.blit(
                user_snake_body_rect, (snake.target_food[0], snake.target_food[1])
            )

        # Check for grid border colision
        if not grid_rect.collidepoint(userSnake.head[0], userSnake.head[1]):
            pygame.quit()
            sys.exit()

        # Check for self colision
        if userSnake.self_colision:
            pygame.quit()
            sys.exit()

        for snake in pySnakes_list:
            if snake.self_colision:
                pySnakes_list.remove(snake)
                pygame.quit()
                sys.exit()
        # Check for pySnake colision
        # for snake in pySnakes_list:
        #     if userSnake.head in snake.body:
        #         pygame.quit()
        #         sys.exit()

        # Update the display
        pygame.display.flip()

        # Use clock to control FPS
        clock.tick(FPS)


if __name__ == "__main__":
    main()
