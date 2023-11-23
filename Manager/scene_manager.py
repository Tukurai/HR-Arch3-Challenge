from Engine.text_component import TextComponent
from Scenes.main_menu_scene import MainMenuScene
from Scenes.race_scene import RaceScene
from Scenes.high_score_scene import HighScoreScene
from Scenes.car_selection_scene import CarSelectionScene


class SceneManager:
    def __init__(self, sound_manager):
        self.scenes = self.create_scenes()
        self.sound_manager = sound_manager

        self.active_scene = self.get_scene_by_name("Main menu")

    def handle_events(self):
        self.active_scene.handle_events()

    def update(self, timedelta, input_state):
        self.active_scene.update(timedelta, input_state)

    def draw(self, screen):
        self.active_scene.draw(screen)

    def set_active_scene(self, scene):
        self.active_scene = scene

    def get_scene_by_name(self, scene_name):
        return next((scene for scene in self.scenes if scene.scene_name == scene_name), None)

    def create_scenes(self):
        # Create a static list of scenes based on the base class GameScene.
        scenes = {
            MainMenuScene(self, [
                TextComponent("Logo", "Fantastic Race Game", None, 200, 60, 0, 0, 0, 1.00)
            ]),
            HighScoreScene(self, {}),
            RaceScene(self, {}),
            CarSelectionScene(self, {}),
        }
        return scenes


if __name__ == "__main__":
    print("Ran scene_manager.py directly. Start application from game.py.")
