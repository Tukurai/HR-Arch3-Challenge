from game_engine import GameEngine
import pygame


class RacingGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1536, 1280))
        pygame.display.set_caption("Racing Game")
        self.clock = pygame.time.Clock()
        self.game_engine = GameEngine(self)

    def run(self):
        while True:
            # Get the timedelta
            timedelta = self.clock.tick(60) / 1000.0

            self.game_engine.handle_events()
            self.game_engine.update(timedelta)
            self.game_engine.draw()


if __name__ == "__main__":
    game = RacingGame()
    game.run()
