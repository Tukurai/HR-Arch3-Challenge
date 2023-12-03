import pygame
from Engine.button_component import BUTTON_CLICK, ButtonComponent
from Engine.text_component import TextComponent
from Scenes.game_scene import GameScene
from Settings import settings
from Settings.user_events import USER_QUIT


class MainMenuScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Main menu", components)

    def handle_event(self, event):
        if event.type == BUTTON_CLICK:
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

    def build_ui(self):
        screen = self.scene_manager.screen

        self.components.extend([
            TextComponent(
                "Header",
                "Fantastic Race Game",
                36,
                True,
                None,
                (screen.get_width() / 2, 200),
                0,
                0,
                0,
                1.00,
            ),
            ButtonComponent(
                "SinglePlayer",
                self.sprite_manager.get_full_ui_element(
                    "blue_button00.png",
                    "green_button00.png",
                    "green_button01.png",
                ),
                (
                    screen.get_width() / 2 - 95,
                    screen.get_height() / 2 - 170,
                ),
                0,
                1,
                "Singleplayer",
                32,
                True,
            ),
            ButtonComponent(
                "MultiPlayer",
                self.sprite_manager.get_full_ui_element(
                    "blue_button00.png",
                    "green_button00.png",
                    "green_button01.png",
                ),
                (
                    screen.get_width() / 2 - 95,
                    screen.get_height() / 2 - 85,
                ),
                0,
                1,
                "Multiplayer",
                32,
                True,
            ),
            ButtonComponent(
                "HighScoreButton",
                self.sprite_manager.get_full_ui_element(
                    "blue_button00.png",
                    "green_button00.png",
                    "green_button01.png",
                ),
                (
                    screen.get_width() / 2 - 95,
                    screen.get_height() / 2,
                ),
                0,
                1,
                "Highscores",
                32,
                True,
            ),
            ButtonComponent(
                "QuitButton",
                self.sprite_manager.get_full_ui_element(
                    "blue_button00.png",
                    "green_button00.png",
                    "green_button01.png",
                ),
                (
                    screen.get_width() / 2 - 95,
                    screen.get_height() / 2 + 85,
                ),
                0,
                1,
                "Quit",
                32,
                True,
            ),
        ])
