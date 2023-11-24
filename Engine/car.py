from Engine.component import Component


class Car(Component):
    def __init__(
        self, max_speed, component_name, full_sprite, x, y, rotation, depth
    ):
        super().__init__(component_name, full_sprite.sprite, x, y, full_sprite.width, full_sprite.height, rotation, depth)
        self.max_speed = max_speed
        self.current_speed = 0

    def handle_event(self, event):
        pass

    def update(self, timedelta, input_state):
        pass

    def draw(self, screen):
        pass

    def move(self):  # By default Car will drive itself
        pass
