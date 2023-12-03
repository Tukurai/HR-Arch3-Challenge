import sys
from Manager.scene_manager import SceneManager
from Manager.server_manager import ServerManager
from Manager.sound_manager import SoundManager
from Manager.sprite_manager import SpriteManager
from Engine.input_state import InputState
import pygame

from Settings import settings
from Settings.user_events import USER_QUIT


class GameEngine:
    def __init__(self, game):
        self.game = game
        self.input_state = InputState(
            None, pygame.key.get_pressed(), None, pygame.mouse.get_pressed()
        )
        self.scene_manager = SceneManager(
            sound_manager=SoundManager(), 
            sprite_manager=SpriteManager(),
            screen=self.game.screen
        )
        self.score_manager = ServerManager()

    def handle_events(self):
        for event in pygame.event.get():  # Handle the close window event.
            if event.type == pygame.QUIT or event.type == USER_QUIT:
                pygame.quit()
                sys.exit()
            else:
                self.scene_manager.handle_event(event)
                self.score_manager.handle_event(event)

    def update(self, timedelta):
        self.input_state.update(
            pygame.key.get_pressed(), pygame.mouse.get_pressed()
        )  # Update current states.
        self.scene_manager.update(timedelta, self.input_state)

    def draw(self):
        self.game.screen.fill((0, 0, 0))  # Fill the screen with black.

        self.scene_manager.draw(self.game.screen)  # Draw any scene related components.

        pygame.display.flip()  # Flip the display


if __name__ == "__main__":
    if(settings.DEBUG_MODE): print("Ran game_engine.py directly. Start application from game.py.")
