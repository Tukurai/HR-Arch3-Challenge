import pygame

from Engine.component import Component


class CarSelectionComponent(Component):
    def __init__(self, player_id: int, file_name: str, pos: tuple[int, int], depth=0.50):
        super().__init__(
            component_name=file_name,
            sprite=None,
            pos=pos,
            width=0,
            height=0,
            rotation=0,
            depth=depth,
            scale=1.0,
        )
        self.components = []
        self.player_id = player_id
        self.build_ui()

    def build_ui(self):
        pass

    def update(self, delta_time, user_input):
        pass

    def handle_event(self, event):
        pass
