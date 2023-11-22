class GameScene:
    def __init__(self, scene_manager, scene_name, components):
        self.scene_manager = scene_manager
        self.scene_name = scene_name
        self.components = components

    def handle_events(self):
        for component in self.components.values():
            component.handle_events()

    def update(self, timedelta, input_state):
        for component in self.components.values():
            component.update(timedelta, input_state)

    def draw(self):
        for component in self.components.values():
            component.draw()
