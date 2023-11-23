class Component:
    def __init__(self, component_name, sprite, x, y, width, height, rotation, depth):
        self.component_name = component_name
        self.sprite = sprite
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.depth = depth

    def handle_event(self, event):
        pass

    def update(self, timedelta, input_state):
        pass

    def draw(self, screen):
        pass
