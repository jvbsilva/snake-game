import random


class Snake:
    def __init__(self, head: list, square_size: int):
        self.head = head
        self.square_size = square_size
        self.body = []
        self.body.append(head)
        self.cur_direction = ""
        self.self_colision = False

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


class PySnake(Snake):
    def __init__(self, head: list, square_size: int):
        super().__init__(head, square_size)
        self.color = (55, 255, 55)
        self.target_food = [0, 0]

    def chose_target_food(self, food_list):
        best_dist = 0
        for food in food_list:
            dist = (abs(self.head[0] - food[0]) + abs(self.head[1] - food[1])) * -1
            if dist < best_dist:
                self.target_food = food

    def chase_food(self):
        possible_moves = ["RIGHT", "LEFT", "UP", "DOWN"]
        if possible_moves:
            self.cur_direction = random.choice(possible_moves)
