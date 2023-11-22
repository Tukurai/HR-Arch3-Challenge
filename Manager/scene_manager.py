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
        self.active_scene.handle_events(self)

    def update(self, timedelta, input_state):
        self.active_scene.update(self, timedelta, input_state)

    def draw(self):
        self.active_scene.draw(self)

    def set_active_scene(self, scene):
        self.active_scene = scene

    def get_scene_by_name(self, scene_name):
        return next((scene for scene in self.scenes if scene.name == scene_name), None)

    def create_scenes(self):
        # Create a static list of scenes based on the base class GameScene.
        scenes = {
            MainMenuScene(self, {}),
            HighScoreScene(self, {}),
            RaceScene(self, {}),
            CarSelectionScene(self, {}),
        }
        return scenes


if __name__ == "__main__":
    print("Ran scene_manager.py directly. Start application from game.py.")
