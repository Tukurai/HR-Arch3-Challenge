import pygame
from Scenes.game_scene import GameScene


class MainMenuScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Main menu", components)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_1:
                selection_scene = self.scene_manager.get_scene_by_name("Car selection")
                selection_scene.selected_cars = []
                self.scene_manager.set_active_scene(selection_scene)
            elif event.key == pygame.K_2:
                selection_scene = self.scene_manager.get_scene_by_name("Car selection")
                selection_scene.selected_cars = []
                selection_scene.cars_needed = 2
                self.scene_manager.set_active_scene(selection_scene)

        return super().handle_event(event)
