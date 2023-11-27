import pygame
from Scenes.game_scene import GameScene


class MainMenuScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Main menu", components)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("Car selection")
                )

        return super().handle_event(event)
