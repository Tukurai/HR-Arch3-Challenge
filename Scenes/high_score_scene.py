from Scenes.game_scene import GameScene


class HighScoreScene(GameScene):
    def __init__(self, scene_manager, components):
        super().__init__(scene_manager, "High score", components)
