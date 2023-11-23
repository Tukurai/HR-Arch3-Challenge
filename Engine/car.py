class Car:
    def __init__(self, component_name, sprite, x, y, width, height, rotation, depth):
        super().__init__(component_name, sprite, x, y, width, height, rotation, depth)

    def handle_events(self):
        pass

    def update(self, timedelta, input_state):
        pass

    def draw(self):
        pass
