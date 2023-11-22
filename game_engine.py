import sys
from Manager.scene_manager import SceneManager
from Engine.input_state import InputState
import pygame


class GameEngine:
    def __init__(self, game):
        self.game = game
        self.input_state = InputState(
            None, pygame.key.get_pressed(), None, pygame.mouse.get_pressed()
        )
        self.scene_manager = SceneManager(sound_manager=None)

    def handle_events(self):
        for event in pygame.event.get():  # Handle the close window event.
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.scene_manager.handle_events()

    def update(self, timedelta):
        self.input_state.update(
            pygame.key.get_pressed(), pygame.mouse.get_pressed()
        )  # Update current states.
        self.scene_manager.update(timedelta, self.input_state)

    def draw(self):
        self.game.screen.fill((0, 0, 0))  # Fill the screen with black.

        self.scene_manager.draw()  # Draw any scene related components.

        pygame.display.flip()  # Flip the display


if __name__ == "__main__":
    print("Ran game_engine.py directly. Start application from game.py.")
