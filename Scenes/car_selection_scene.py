import pygame
from Scenes.game_scene import GameScene


class CarSelectionScene(GameScene):
    def __init__(self, scene_manager, components):
        super().__init__(scene_manager, "Car selection", components)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_1
                or event.key == pygame.K_2
                or event.key == pygame.K_3
                or event.key == pygame.K_4
            ):
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("Race")
                )

        return super().handle_event(event)
