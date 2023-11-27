class GameScene:
    def __init__(self, scene_manager, sprite_manager, scene_name, components):
        self.scene_manager = scene_manager
        self.sprite_manager = sprite_manager
        self.scene_name = scene_name
        self.components = components

    def handle_event(self, event):
        for component in self.components:
            component.handle_event(event)

    def update(self, timedelta, input_state):
        for component in self.components:
            component.update(timedelta, input_state)

    def draw(self, screen):
        for component in self.components:
            component.draw(screen)
