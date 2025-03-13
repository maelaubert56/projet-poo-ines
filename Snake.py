from Element import Element

class Snake(Element):
    def __init__(self, size=3, speed=150, direction='Right', is_head=False, is_food=False, is_dead=False):
        super().__init__('H' if is_head else 'S')  # Different symbols for head and body
        self.size = size
        self.speed = speed
        self.direction = direction
        self.is_head = is_head
        self.is_food = is_food
        self.is_dead = is_dead