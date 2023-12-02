import pygame
from Engine.component import Component
from Engine.text_component import TextComponent
from Engine.button_component import ButtonComponent
from Engine.text_box import TextBox
from Scenes.main_menu_scene import MainMenuScene
from Scenes.race_scene import RaceScene
from Scenes.high_score_scene import HighScoreScene
from Scenes.car_selection_scene import CarSelectionScene
from Settings import settings


class SceneManager:
    def __init__(self, sound_manager, sprite_manager, screen):
        self.sound_manager = sound_manager
        self.sprite_manager = sprite_manager
        self.screen = screen

        self.scenes = self.create_scenes()
        self.set_active_scene(self.get_scene_by_name("Main menu"))

    def handle_event(self, event):
        self.active_scene.handle_event(event)
        self.sound_manager.handle_event(event)

    def update(self, timedelta, input_state):
        self.active_scene.update(timedelta, input_state)

    def draw(self, screen):
        self.active_scene.draw(screen)

    def set_active_scene(self, scene):
        self.active_scene = scene
        self.active_scene.scene_changed()

    def get_scene_by_name(self, scene_name):
        return next(
            (scene for scene in self.scenes if scene.scene_name == scene_name), None
        )

    def create_scenes(self):
        # Create a static list of scenes based on the base class GameScene.
        scenes = {
            MainMenuScene(
                self,
                self.sprite_manager,
                [
                    TextComponent(
                        "Header",
                        "Fantastic Race Game",
                        36,
                        True,
                        None,
                        (self.screen.get_width() / 2, 200),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    ButtonComponent(
                        "SinglePlayer",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width() / 2 - 95,
                            self.screen.get_height() / 2 - 170,
                        ),
                        self.sprite_manager.get_ui_element("blue_button00.png").width,
                        self.sprite_manager.get_ui_element("blue_button00.png").height,
                        0,
                        1,
                        "Singleplayer",
                        32,
                        True,
                    ),
                    ButtonComponent(
                        "MultiPlayer",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width() / 2 - 95,
                            self.screen.get_height() / 2 - 85,
                        ),
                        self.sprite_manager.get_ui_element("blue_button00.png").width,
                        self.sprite_manager.get_ui_element("blue_button00.png").height,
                        0,
                        1,
                        "Multiplayer",
                        32,
                        True,
                    ),
                    ButtonComponent(
                        "HighScoreButton",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width() / 2 - 95,
                            self.screen.get_height() / 2,
                        ),
                        self.sprite_manager.get_ui_element("blue_button00.png").width,
                        self.sprite_manager.get_ui_element("blue_button00.png").height,
                        0,
                        1,
                        "Highscores",
                        32,
                        True,
                    ),
                    ButtonComponent(
                        "QuitButton",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width() / 2 - 95,
                            self.screen.get_height() / 2 + 85,
                        ),
                        self.sprite_manager.get_ui_element("blue_button00.png").width,
                        self.sprite_manager.get_ui_element("blue_button00.png").height,
                        0,
                        1,
                        "Quit",
                        32,
                        True,
                    ),
                ],
            ),
            CarSelectionScene(
                self,
                self.sprite_manager,
                [
                    TextComponent(
                        "Header",
                        "Select a car",
                        36,
                        True,
                        None,
                        (self.screen.get_width() / 2, 200),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    TextComponent(
                        "Instruction",
                        "Enter your name, hit enter and select a car",
                        24,
                        True,
                        None,
                        (self.screen.get_width() / 2, self.screen.get_height() - 200),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    ButtonComponent(
                        "BackButton",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width()
                            - self.sprite_manager.get_ui_element(
                                "blue_button00.png"
                            ).width
                            - 220,
                            self.screen.get_height()
                            - self.sprite_manager.get_ui_element(
                                "blue_button00.png"
                            ).height
                            - 150,
                        ),
                        self.sprite_manager.get_ui_element("blue_button00.png").width,
                        self.sprite_manager.get_ui_element("blue_button00.png").height,
                        0,
                        1,
                        "Back to main menu",
                        24,
                        True,
                    ),
                    TextBox(
                        "NameTextBox",
                        (
                            self.screen.get_width() / 2 - 95,
                            self.screen.get_height() / 2 - 255,
                        ),
                        190,
                        49,
                        text="Enter your name",
                        font_size=32,
                        saved_text_display=TextComponent(
                            "PlayerName",
                            "Player Name: ",
                            24,
                            True,
                            None,
                            (
                                self.screen.get_width() / 2,
                                (self.screen.get_height() / 2) - 185,
                            ),
                            0,
                            0,
                            0,
                            1.00,
                        ),
                    ),
                    ButtonComponent(
                        "car1",
                        self.sprite_manager.get_car("car_black_small_1.png").sprite,
                        (
                            (self.screen.get_width() / 2)
                            - (
                                self.sprite_manager.get_car(
                                    "car_black_small_1.png"
                                ).width
                                / 2
                            )
                            - 200,
                            self.screen.get_height() / 2,
                        ),
                        self.sprite_manager.get_car("car_black_small_1.png").width,
                        self.sprite_manager.get_car("car_black_small_1.png").height,
                        0,
                        1.00,
                        "",
                        1,
                        True,
                    ),
                    ButtonComponent(
                        "car2",
                        self.sprite_manager.get_car("car_red_small_1.png").sprite,
                        (
                            (self.screen.get_width() / 2)
                            - (
                                self.sprite_manager.get_car("car_red_small_1.png").width
                                / 2
                            )
                            - 100,
                            self.screen.get_height() / 2,
                        ),
                        self.sprite_manager.get_car("car_red_small_1.png").width,
                        self.sprite_manager.get_car("car_red_small_1.png").height,
                        0,
                        1.00,
                        "",
                        1,
                        True,
                    ),
                    ButtonComponent(
                        "car3",
                        self.sprite_manager.get_car("car_yellow_small_1.png").sprite,
                        (
                            (self.screen.get_width() / 2)
                            - (
                                self.sprite_manager.get_car(
                                    "car_yellow_small_1.png"
                                ).width
                                / 2
                            ),
                            self.screen.get_height() / 2,
                        ),
                        self.sprite_manager.get_car("car_yellow_small_1.png").width,
                        self.sprite_manager.get_car("car_yellow_small_1.png").height,
                        0,
                        1.00,
                        "",
                        1,
                        True,
                    ),
                    ButtonComponent(
                        "car4",
                        self.sprite_manager.get_car("car_green_small_1.png").sprite,
                        (
                            (self.screen.get_width() / 2)
                            - (
                                self.sprite_manager.get_car(
                                    "car_green_small_1.png"
                                ).width
                                / 2
                            )
                            + 100,
                            self.screen.get_height() / 2,
                        ),
                        self.sprite_manager.get_car("car_green_small_1.png").width,
                        self.sprite_manager.get_car("car_green_small_1.png").height,
                        0,
                        1.00,
                        "",
                        1,
                        True,
                    ),
                    ButtonComponent(
                        "car5",
                        self.sprite_manager.get_car("car_blue_small_1.png").sprite,
                        (
                            (self.screen.get_width() / 2)
                            - (
                                self.sprite_manager.get_car(
                                    "car_blue_small_1.png"
                                ).width
                                / 2
                            )
                            + 200,
                            self.screen.get_height() / 2,
                        ),
                        self.sprite_manager.get_car("car_blue_small_1.png").width,
                        self.sprite_manager.get_car("car_blue_small_1.png").height,
                        0,
                        1.00,
                        "",
                        1,
                        True,
                    ),
                ],
            ),
            RaceScene(
                self,
                self.sprite_manager,
                [
                    TextComponent(
                        "Header",
                        "Race",
                        36,
                        True,
                        None,
                        (self.screen.get_width() / 2, 32),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    TextComponent(
                        "Instruction",
                        "Use W, A, S, D to control your car",
                        24,
                        True,
                        None,
                        (self.screen.get_width() / 2, self.screen.get_height() - 60),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    ButtonComponent(
                        "EndRaceButton",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width()
                            - self.sprite_manager.get_ui_element(
                                "blue_button00.png"
                            ).width
                            - 220,
                            self.screen.get_height()
                            - self.sprite_manager.get_ui_element(
                                "blue_button00.png"
                            ).height
                            - 150,
                        ),
                        self.sprite_manager.get_ui_element("blue_button00.png").width,
                        self.sprite_manager.get_ui_element("blue_button00.png").height,
                        0,
                        1,
                        "End Race",
                        24,
                        True,
                    ),
                ],
            ),
            HighScoreScene(
                self,
                self.sprite_manager,
                [
                    TextComponent(
                        "Header",
                        "High Scores",
                        36,
                        True,
                        None,
                        (self.screen.get_width() / 2, 200),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    ButtonComponent(
                        "BackButton",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width()
                            - self.sprite_manager.get_ui_element(
                                "blue_button00.png"
                            ).width
                            - 220,
                            self.screen.get_height()
                            - self.sprite_manager.get_ui_element(
                                "blue_button00.png"
                            ).height
                            - 150,
                        ),
                        self.sprite_manager.get_ui_element("blue_button00.png").width,
                        self.sprite_manager.get_ui_element("blue_button00.png").height,
                        0,
                        1,
                        "Back to main menu",
                        24,
                        True,
                    ),
                ],
            ),
        }
        return scenes


if __name__ == "__main__":
    if settings.DEBUG_MODE:
        print("Ran scene_manager.py directly. Start application from game.py.")
