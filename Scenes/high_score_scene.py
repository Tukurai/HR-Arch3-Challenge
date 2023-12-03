import pygame
from Engine.text_component import TextComponent
from Scenes.game_scene import GameScene
from Engine.button_component import BUTTON_CLICK, ButtonComponent
from Settings.user_events import SUBMIT_SCORE_EVENT


class HighScoreScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "High score", components)
        self.score_manager = self.scene_manager.score_manager

    def handle_event(self, event):
        if event.type == BUTTON_CLICK:
            if event.button.component_name == "BackButton":
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("Main menu")
                )
        if event.type == SUBMIT_SCORE_EVENT:
            self.build_ui()

        return super().handle_event(event)

    def build_ui(self):
        screen = self.scene_manager.screen

        text_component_settings = {
            1: ["FirstPlace", 300],
            2: ["SecondPlace", 340],
            3: ["ThirdPlace", 380],
            4: ["FourthPlace", 420],
            5: ["FifthPlace", 460],
            6: ["SixthPlace", 500],
            7: ["SeventhPlace", 540],
            8: ["EithPlace", 580],
            9: ["NinthPlace", 620],
            10: ["TenthPlace", 660],
        }

        text_components = [
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

        player_scores = {}
        print(player_scores)
        for map_data in self.scene_manager.scores.values():
            for player_data in map_data:
                player_scores[player_data[1]] = player_data[0]

        sorted_dict = {
            key: value
            for key, value in sorted(player_scores.items(), key=lambda item: item[1])
        }

        index = 1
        for key, value in sorted_dict.items():
            print(text_component_settings[index][1])
            text_components.append(
                TextComponent(
                    text_component_settings[index][0],
                    f"{index}: " + key + " - " + str(value),
                    30,
                    True,
                    None,
                    (screen.get_width() / 2, text_component_settings[index][1]),
                    0,
                    0,
                    0,
                    1.00,
                ),
            )
            index += 1

        index = 0
        self.components.extend(text_components)
