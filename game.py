import pygame
import sys


class GameManager:
    def __init__(self, game):
        self.game = game
        # TODO: Initialize other game objects and managers

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # TODO: Delegate event handling to other managers

    def update(self, timedelta):
        print(f"td: {timedelta} seconds")
        # TODO: Update game objects and managers

    def draw(self):
        self.game.screen.fill((0, 0, 0))  # Fill  the screen with black.
        # TODO: Draw game objects and managers
        pygame.display.flip()  # Flip the display


class RacingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Racing Game")
        self.clock = pygame.time.Clock()
        self.game_manager = GameManager(self)

    def run(self):
        while True:
            # Get the timedelta
            timedelta = self.clock.tick(60) / 1000.0

            self.game_manager.handle_events()
            self.game_manager.update(timedelta)
            self.game_manager.draw()


if __name__ == "__main__":
    game = RacingGame()
    game.run()
