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

        self.components.extend(
            [
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
                TextComponent(
                    "FirstPlace",
                    "1: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 300),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "SecondPlace",
                    "2: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 340),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "ThirdPlace",
                    "3: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 380),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "FourthPlace",
                    "4: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 420),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "FifthPlace",
                    "5: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 460),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "SixthPlace",
                    "6: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 500),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "SeventhPlace",
                    "7: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 540),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "EithPlace",
                    "8: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 580),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "NinthPlace",
                    "9: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 620),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "TenthPlace",
                    "10: ",
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, 660),
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
                        - self.sprite_manager.get_ui_element("blue_button00.png").width
                        - 220,
                        screen.get_height()
                        - self.sprite_manager.get_ui_element("blue_button00.png").height
                        - 150,
                    ),
                    0,
                    1,
                    "Back to main menu",
                    24,
                    True,
                ),
            ]
        )
