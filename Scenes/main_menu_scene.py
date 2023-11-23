from Scenes.game_scene import GameScene


class MainMenuScene(GameScene):
    def __init__(self, scene_manager, components):
        super().__init__(scene_manager, "Main menu", components)
