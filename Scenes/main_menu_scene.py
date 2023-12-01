import pygame
from Engine.button_component import BUTTON_COLLISION
from Scenes.game_scene import GameScene
from Settings import settings

USER_QUIT = pygame.USEREVENT + 3

class MainMenuScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Main menu", components)

    def handle_event(self, event):
        if event.type == BUTTON_COLLISION:
            if pygame.mouse.get_pressed()[0]:
                if event.button.component_name == "SinglePlayer":
                    selection_scene = self.scene_manager.get_scene_by_name(
                        "Car selection"
                    )
                    selection_scene.selected_cars = []
                    self.scene_manager.set_active_scene(selection_scene)
                elif event.button.component_name == "MultiPlayer":
                    selection_scene = self.scene_manager.get_scene_by_name(
                        "Car selection"
                    )
                    selection_scene.selected_cars = []
                    selection_scene.cars_needed = 2
                    self.scene_manager.set_active_scene(selection_scene)
                elif event.button.component_name == "HighScoreButton":
                    self.scene_manager.set_active_scene(
                        self.scene_manager.get_scene_by_name("High score")
                    )
                elif event.button.component_name == "QuitButton":
                    user_quit = pygame.event.Event(USER_QUIT, quit=True)
                    pygame.event.post(user_quit)

                if(settings.DEBUG_MODE): print(f"Button {event.button.component_name} clicked!")

        return super().handle_event(event)
