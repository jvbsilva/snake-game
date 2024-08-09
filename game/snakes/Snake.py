class Snake:
    def __init__(self, head: list, square_size: int):
        self.head = head
        self.square_size = square_size
        self.body = []
        self.body.append(head)
        self.cur_direction = ""

    def turn(self, direction: str):
        self.cur_direction = direction

    def move_right(self):
        self.head[0] += self.square_size

    def move_left(self):
        self.head[0] -= self.square_size

    def move_up(self):
        self.head[1] -= self.square_size

    def move_down(self):
        self.head[1] += self.square_size

    def move(self):
        if self.cur_direction == "RIGHT":
            self.move_right()
        elif self.cur_direction == "LEFT":
            self.move_left()
        elif self.cur_direction == "UP":
            self.move_up()
        elif self.cur_direction == "DOWN":
            self.move_down()
        else:
            pass
