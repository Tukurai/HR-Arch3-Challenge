class Component:
    def __init__(self, component_name, sprite, x, y, width, height, rotation):
        self.component_name = component_name
        self.sprite = sprite
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation

    def handle_events(self):
        print(
            f"DEBUG: {self.component_name} triggered 'handle_events()'."
        )

    def update(self, timedelta, input_state):
        print(
            f"DEBUG: {self.component_name} triggered 'update({timedelta}, {input_state})'."
        )

    def draw(self):
        print(
            f"DEBUG: {self.component_name} triggered 'draw()'."
        )
