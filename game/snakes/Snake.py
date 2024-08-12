import random


class Snake:
    def __init__(self, head: list, square_size: int):
        self.head = head
        self.square_size = square_size
        self.body = []
        self.body.append(head)
        self.cur_direction = ""
        self.self_colision = False

    def move(self):
        new_head = self.head.copy()

        if self.cur_direction == "RIGHT":
            new_head[0] += self.square_size
        elif self.cur_direction == "LEFT":
            new_head[0] -= self.square_size
        elif self.cur_direction == "UP":
            new_head[1] -= self.square_size
        elif self.cur_direction == "DOWN":
            new_head[1] += self.square_size
        else:
            pass

        if len(self.body) > 1:
            if new_head in self.body:
                self.self_colision = True

        self.head = new_head
        self.body.insert(0, new_head)
        self.body.pop()

    def eat(self, food):
        self.body.append(food)


class UserSnake(Snake):
    def __init__(self, head: list, square_size: int):
        super().__init__(head, square_size)

    def turn(self, direction: str):
        if self.cur_direction == "RIGHT" and direction == "LEFT":
            return
        elif self.cur_direction == "LEFT" and direction == "RIGHT":
            return
        elif self.cur_direction == "UP" and direction == "DOWN":
            return
        elif self.cur_direction == "DOWN" and direction == "UP":
            return
        else:
            self.cur_direction = direction


class PySnake(Snake):
    def __init__(self, head: list, square_size: int):
        super().__init__(head, square_size)
        self.target_food = [0, 0]

    def chose_target_food(self, food_list):
        if self.target_food not in food_list:
            best_dist = float("inf")
            for food in food_list:
                dist = abs(self.head[0] - food[0]) + abs(self.head[1] - food[1])
                if dist < best_dist:
                    self.target_food = food
                    best_dist = dist

    def look(self, direction: str):
        if direction == "RIGHT":
            return [self.head[0] + self.square_size, self.head[1]]
        elif direction == "LEFT":
            return [self.head[0] - self.square_size, self.head[1]]
        elif direction == "UP":
            return [self.head[0], self.head[1] - self.square_size]
        elif direction == "DOWN":
            return [self.head[0], self.head[1] + self.square_size]
        else:
            return None

    def chase_food(self):
        possible_moves = ["UP", "DOWN", "RIGHT", "LEFT"]
        best_move = ""
        best_dist = float("inf")
        for move in possible_moves:
            next_point = self.look(move)
            if next_point not in self.body:
                dist = abs(next_point[0] - self.target_food[0]) + abs(
                    next_point[1] - self.target_food[1]
                )
                if dist < best_dist:
                    best_move = move
                    best_dist = dist
        if best_move:
            self.cur_direction = best_move
