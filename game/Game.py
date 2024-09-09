import random
from Snakes import UserSnake, PySnake


class Game:
    def __init__(
        self, n_snakes: int, n_foods: int, width: int, height: int, square_size: int
    ):
        self.n_snakes = n_snakes
        self.n_foods = n_foods
        self.width = width
        self.height = height
        self.square_size = square_size

        self.grid = [
            (x, y)
            for x in range(0, width, square_size)
            for y in range(0, height, square_size)
        ]
        self.available_points = self.grid.copy()
        self.food_list = [self.use_available_point() for _ in range(n_foods)]
        self.available_food_list = self.food_list.copy()
        self.py_snakes_list = [
            PySnake(self.use_available_point(), square_size) for _ in range(n_snakes)
        ]
        self.user_snake = UserSnake(self.use_available_point(), square_size)

        for snake in self.py_snakes_list:
            snake.chose_target_food(self.available_food_list)
            self.available_food_list.remove(snake.target_food)

        self.update_available_points()

    def use_available_point(self):
        point = random.choice(self.available_points)
        self.available_points.remove(point)
        return list(point)

    def get_occupied_points(self):
        occupied_points = []
        occupied_points.extend(self.user_snake.body)
        for snake in self.py_snakes_list:
            occupied_points.extend(snake.body)
        occupied_points.extend(self.food_list)
        occupied_points = [(point[0], point[1]) for point in occupied_points]
        return occupied_points

    def update_available_points(self):
        self.available_points = [
            point
            for point in self.grid.copy()
            if point not in self.get_occupied_points()
        ]

    def move_snakes(self):
        self.user_snake.move()
        for snake in self.py_snakes_list:
            snake.chase_food(self.available_points)
            snake.move()

    def feed_snakes(self):

        user_ate, food_eaten = False, False
        for food in self.food_list:
            if self.user_snake.can_eat(food):
                self.user_snake.eat()
                self.food_list.remove(self.user_snake.head)
                user_ate = True
                food_eaten = True
            else:
                for snake in self.py_snakes_list:
                    if snake.can_eat(food):
                        snake.eat()
                        food_eaten = True
                        self.food_list.remove(snake.head)
                        break
        if food_eaten:
            self.after_food_eaten()

        return user_ate

    def after_food_eaten(self):
        self.update_available_points()
        while len(self.food_list) < self.n_foods:
            self.food_list.append(self.use_available_point())
        self.available_food_list = self.food_list.copy()
        for snake in self.py_snakes_list:
            snake.chose_target_food(self.available_food_list)
            self.available_food_list.remove(snake.target_food)

    def prepare_for_next_iteration(self):
        self.update_available_points()
        self.py_snakes_list.sort(key=lambda x: len(x.body), reverse=False)
