import pygame
from Engine.component import Component
from Engine.text_component import TextComponent
from Engine.button_component import ButtonComponent
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
                        (self.screen.get_width() / 2, 32),
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
                        190,
                        49,
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
                        190,
                        49,
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
                        190,
                        49,
                        0,
                        1,
                        "Highscores",
                        32,
                        True,
                    ),
                    ButtonComponent(
                        "SettingsButton",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width() / 2 - 95,
                            self.screen.get_height() / 2 + 85,
                        ),
                        190,
                        49,
                        0,
                        1,
                        "Settings",
                        32,
                        True,
                    ),
                    ButtonComponent(
                        "QuitButton",
                        self.sprite_manager.get_ui_element("blue_button00.png").sprite,
                        (
                            self.screen.get_width() / 2 - 95,
                            self.screen.get_height() / 2 + 170,
                        ),
                        190,
                        49,
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
                        (self.screen.get_width() / 2, 32),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    TextComponent(
                        "Instruction",
                        "Press 1, 2, 3, 4 or 5 to choose",
                        24,
                        True,
                        None,
                        (self.screen.get_width() / 2, self.screen.get_height() - 60),
                        0,
                        0,
                        0,
                        1.00,
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
                        (self.screen.get_width() / 2, 32),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    TextComponent(
                        "Instruction",
                        "Press Enter to to back to the main menu",
                        24,
                        True,
                        None,
                        (self.screen.get_width() / 2, self.screen.get_height() - 60),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                ],
            ),
        }
        return scenes


if __name__ == "__main__":
    if(settings.DEBUG_MODE): print("Ran scene_manager.py directly. Start application from game.py.")
