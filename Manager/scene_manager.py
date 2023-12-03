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
            MainMenuScene(self, self.sprite_manager, []),
            CarSelectionScene(self,self.sprite_manager, []),
            RaceScene(self,self.sprite_manager,[]),
            HighScoreScene(self,self.sprite_manager,[]),
        }
        return scenes


if __name__ == "__main__":
    if settings.DEBUG_MODE:
        print("Ran scene_manager.py directly. Start application from game.py.")
