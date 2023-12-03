import pygame
from Engine.text_component import TextComponent
from Scenes.game_scene import GameScene
from Engine.button_component import BUTTON_CLICK, ButtonComponent

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
    
    def build_ui(self):
        screen = self.scene_manager.screen

        self.components.extend([
            TextComponent(
                "Header",
                "High Scores",
                36,
                True,
                None,
                (screen.get_width() / 2, 200),
                0,
                0,
                0,
                1.00,
            ),
            ButtonComponent(
                "BackButton",
                self.sprite_manager.get_full_ui_element(
                    "blue_button00.png",
                    "green_button00.png",
                    "green_button01.png",
                ),
                (
                    screen.get_width()
                    - self.sprite_manager.get_ui_element(
                        "blue_button00.png"
                    ).width
                    - 220,
                    screen.get_height()
                    - self.sprite_manager.get_ui_element(
                        "blue_button00.png"
                    ).height
                    - 150,
                ),
                0,
                1,
                "Back to main menu",
                24,
                True,
            ),
        ])
