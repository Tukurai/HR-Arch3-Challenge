import pygame
from Engine.player_car import PlayerCar
from Engine.text_component import TextComponent
from Enums.direction import Direction
from Scenes.main_menu_scene import MainMenuScene
from Scenes.race_scene import RaceScene
from Scenes.high_score_scene import HighScoreScene
from Scenes.car_selection_scene import CarSelectionScene


class SceneManager:
    def __init__(self, sound_manager):
        self.scenes = self.create_scenes()
        self.sound_manager = sound_manager

        self.active_scene = self.get_scene_by_name("Main menu")

    def handle_event(self, event):
        self.active_scene.handle_event(event)

    def update(self, timedelta, input_state):
        self.active_scene.update(timedelta, input_state)

    def draw(self, screen):
        self.active_scene.draw(screen)

    def set_active_scene(self, scene):
        self.active_scene = scene

    def get_scene_by_name(self, scene_name):
        return next(
            (scene for scene in self.scenes if scene.scene_name == scene_name), None
        )

    def create_scenes(self):
        # Create a static list of scenes based on the base class GameScene.
        scenes = {
            MainMenuScene(
                self,
                [
                    TextComponent(
                        "Header",
                        "Fantastic Race Game",
                        36,
                        True,
                        None,
                        400,
                        60,
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    TextComponent(
                        "Instruction",
                        "Press Enter to play",
                        24,
                        True,
                        None,
                        400,
                        500,
                        0,
                        0,
                        0,
                        1.00,
                    ),
                ],
            ),
            CarSelectionScene(
                self,
                [
                    TextComponent(
                        "Header", "Select a car", 36, True, None, 400, 60, 0, 0, 0, 1.00
                    ),
                    TextComponent(
                        "Instruction",
                        "Press 1, 2, 3 or 4 to choose",
                        24,
                        True,
                        None,
                        400,
                        500,
                        0,
                        0,
                        0,
                        1.00,
                    ),
                ],
            ),
            RaceScene(
                self,
                [
                    TextComponent(
                        "Header", "Race", 36, True, None, 400, 60, 0, 0, 0, 1.00
                    ),
                    TextComponent(
                        "Instruction",
                        "Use W, A, S, D to control your car",
                        24,
                        True,
                        None,
                        400,
                        500,
                        0,
                        0,
                        0,
                        1.00,
                    ),
                    PlayerCar(
                        "Player",
                        {
                            pygame.K_w: Direction.UP,
                            pygame.K_a: Direction.LEFT,
                            pygame.K_s: Direction.DOWN,
                            pygame.K_d: Direction.RIGHT,
                        },
                        180,
                        "Player Car",
                        None,
                        400,
                        250,
                        40,
                        80,
                        0,
                        1.10,
                    ),
                ],
            ),
            HighScoreScene(
                self,
                [
                    TextComponent(
                        "Header", "High Scores", 36, True, None, 400, 60, 0, 0, 0, 1.00
                    ),
                    TextComponent(
                        "Instruction",
                        "Press Enter to to back to the main menu",
                        24,
                        True,
                        None,
                        400,
                        500,
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
    print("Ran scene_manager.py directly. Start application from game.py.")
