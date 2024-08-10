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
