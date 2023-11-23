import pygame
from Scenes.game_scene import GameScene


class RaceScene(GameScene):
    def __init__(self, scene_manager, components):
        super().__init__(scene_manager, "Race", components)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("High score")
                )
        
        for component in self.components:
            component.handle_event(event)

        return super().handle_event(event)
