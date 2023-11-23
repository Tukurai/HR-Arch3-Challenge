import pygame
from Scenes.game_scene import GameScene


class RaceScene(GameScene):
    def __init__(self, scene_manager, components):
        super().__init__(scene_manager, "Race", components)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_w
                or event.key == pygame.K_a
                or event.key == pygame.K_s
                or event.key == pygame.K_d
            ):
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("High score")
                )

        return super().handle_event(event)
