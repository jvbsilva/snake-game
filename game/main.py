import pygame
from pygame.surface import Surface
from pygame.font import Font
import sys
from Snakes import Snake, UserSnake
from Game import Game

FPS = 10
N_FOODS = 5
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
ORANGE = (255, 165, 0)
BLUE = (55, 55, 255)
GREEN = (0, 225, 0)
DARK_GREEN = (0, 125, 0)
PURPLE = (125, 0, 125)


## Auxiliary functions ##


def get_best_score():
    best_score = 0
    try:
        with open("best_score.txt", "r") as file:
            line = file.readline().split()
            best_score = int(line[-1])
    except Exception as e:
        print(e)
    return best_score


def save_best_score(score: int):
    try:
        with open("best_score.txt", "w") as file:
            file.write(f"Best score: {score}")
    except Exception as e:
        print(e)


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


def draw_snake(screen: Surface, snake: Snake, body_surf: Surface, head_surf: Surface):
    for piece in snake.body:
        screen.blit(body_surf, (piece[0], piece[1]))
    screen.blit(head_surf, (snake.head[0], snake.head[1]))


def draw_messages(
    is_running: bool,
    screen: Surface,
    speed_msg: Surface,
    points_msg: Surface,
    press_any_key_msg: Surface,
    best_score_msg: Surface,
):
    if is_running:

        screen.blit(speed_msg, (GRID_WIDTH, 10))
        screen.blit(points_msg, (GRID_WIDTH, 30))
    else:
        screen.blit(press_any_key_msg, (GRID_WIDTH, 10))
        screen.blit(best_score_msg, (GRID_WIDTH, GRID_HEIGHT - 30))


def update_speed_msg(
    speed: int, last_rendered_speed: int, font: Font, speed_msg: Surface
):
    if last_rendered_speed != speed:
        last_rendered_speed = speed
        speed_msg = font.render(f"Speed: {last_rendered_speed}", False, BLACK, None)
    return speed_msg


def close(userSnake: UserSnake, best_score):
    if userSnake.points > best_score:
        save_best_score(userSnake.points)
    pygame.quit()
    sys.exit()


## Auxiliary objects ##

# Create grid surface
grid_surface = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
grid_surface.fill(LIGHT_GREY)
for x, y in GRID_WHITE:
    pygame.draw.rect(
        grid_surface, WHITE_SMOKE, pygame.Rect(x, y, GRID_SQUARE, GRID_SQUARE)
    )

# Create grid rect for colision check
grid_rect = pygame.Rect(0, 0, GRID_WIDTH, GRID_HEIGHT)


user_snake_body_rect = create_rect_with_border(
    GRID_SQUARE, GRID_SQUARE, ORANGE, BLACK, 2
)
user_snake_head_rect = create_rect_with_border(GRID_SQUARE, GRID_SQUARE, RED, BLACK, 2)

pySnake_body_rect = create_rect_with_border(GRID_SQUARE, GRID_SQUARE, GREEN, BLACK, 2)
pySnake_head_rect = create_rect_with_border(
    GRID_SQUARE, GRID_SQUARE, DARK_GREEN, BLACK, 2
)

food_rect = create_rect_with_border(GRID_SQUARE, GRID_SQUARE, BLUE, BLACK, 2)

debug_rect = create_rect_with_border(GRID_SQUARE, GRID_SQUARE, PURPLE, BLACK, 0)


## Main loop ##
def main():

    best_score = get_best_score()

    # Create game
    game = Game(N_PYSNAKES, N_FOODS, GRID_WIDTH, GRID_HEIGHT, GRID_SQUARE)

    # Initialize PyGame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCRERN_HEIGHT))
    pygame.display.set_caption("PySnake")

    # Track initial speed
    speed = FPS
    last_rendered_speed = FPS

    # Create default font
    pygame.font.init()
    my_font = pygame.font.SysFont("Arial", 18, bold=True)

    # Create messages
    press_any_key_msg = my_font.render("Press any key to start", False, BLACK, None)
    speed_msg = my_font.render(f"Speed: {last_rendered_speed}", False, BLACK, None)
    points_msg = my_font.render(f"Poitns: {game.user_snake.points}", False, BLACK, None)
    best_score_msg = my_font.render(f"Best score: {best_score}", False, BLACK, None)

    # Create clock to control fps
    clock = pygame.time.Clock()

    # Main loop
    running = False
    while True:

        # Read events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close(game.user_snake, best_score)

            elif event.type == pygame.KEYDOWN:
                running = True
                if event.key == pygame.K_LEFT:
                    game.user_snake.turn("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.user_snake.turn("RIGHT")
                elif event.key == pygame.K_UP:
                    game.user_snake.turn("UP")
                elif event.key == pygame.K_DOWN:
                    game.user_snake.turn("DOWN")

        if running:
            game.move_snakes()
            user_ate = game.feed_snakes()
            if user_ate:
                # Update points msg
                game.user_snake.points += speed
                points_msg = my_font.render(
                    f"Poitns: {game.user_snake.points}", False, BLACK, None
                )

        # Clean the screen
        screen.fill(WHITE)

        # Draw the grid
        screen.blit(grid_surface, (0, 0))

        # Draw messages
        speed_msg = update_speed_msg(speed, last_rendered_speed, my_font, speed_msg)
        draw_messages(
            running,
            screen,
            speed_msg,
            points_msg,
            press_any_key_msg,
            best_score_msg,
        )

        # Draw foods
        for food in game.food_list:
            screen.blit(food_rect, (food[0], food[1]))

        # Draw user snake
        draw_snake(screen, game.user_snake, user_snake_body_rect, user_snake_head_rect)

        # Draw pySnakes
        for snake in game.py_snakes_list:
            draw_snake(screen, snake, pySnake_body_rect, pySnake_head_rect)

        # Debug avialable_points
        # for point in game.available_points:
        #     screen.blit(debug_rect, point)

        # Debug target_food
        # for snake in pySnakes_list:
        #     screen.blit(
        #         user_snake_body_rect, (snake.target_food[0], snake.target_food[1])
        #     )

        # Check for colision
        if game.user_snake.self_colision or not grid_rect.collidepoint(
            game.user_snake.head[0], game.user_snake.head[1]
        ):
            close(game.user_snake, best_score)

        for snake in game.py_snakes_list:
            if game.user_snake.head in snake.body:
                close(game.user_snake, best_score)
            if (
                not grid_rect.collidepoint(snake.head[0], snake.head[1])
                or snake.self_colision
            ):
                game.py_snakes_list.remove(snake)

        # Update the display
        pygame.display.flip()

        # Get ready for next iteration
        game.prepare_for_next_iteration()
        speed = FPS + (FPS // N_PYSNAKES) * (N_PYSNAKES - len(game.py_snakes_list))
        # Use clock to control FPS
        clock.tick(speed)


if __name__ == "__main__":
    main()
