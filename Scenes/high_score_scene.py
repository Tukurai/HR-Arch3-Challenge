import pygame
from Scenes.game_scene import GameScene
from Engine.button_component import BUTTON_CLICK

class HighScoreScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "High score", components)

    def handle_event(self, event):
        if event.type == BUTTON_CLICK:
            if event.button.component_name == "BackButton":
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("Main menu")
                )

        return super().handle_event(event)
