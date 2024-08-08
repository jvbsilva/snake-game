
class Snake():
    def __init__(self,head: list, square_size: int):
        self.head = head
        self.square_size = square_size
        self.body = []
        self.body.append(head)
        
    def move_right(self):
        self.head[0] += self.square_size
        
    def move_left(self):
        self.head[0] -= self.square_size
    
    def move_up(self):
        self.head[1] -= self.square_size
    
    def move_down(self):
        self.head[1] += self.square_size

