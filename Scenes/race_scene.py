from Manager.collision_manager import CollisionManager
from Manager.level_manager import LevelManager
import pygame
from Engine.car import Car
from Scenes.game_scene import GameScene


class RaceScene(GameScene):
    def __init__(self, scene_manager, components):
        super().__init__(scene_manager, "Race", components)
        self.level_manager = LevelManager()
        self.collision_manager = CollisionManager()
        self.players = {}

        self.set_level("testmap")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("High score")
                )

        for component in self.components:  # Ignoring level objs.
            component.handle_event(event)

        return super().handle_event(event)

    def update(self, timedelta, input_state):
        for component in self.components:
            component.update(timedelta, input_state)

    def draw(self, screen):
        for component in self.components:
            component.draw(screen)
        
        for tile in self.level['Roads']:
            tile.draw(screen)
        
        for object in self.level['Objects']:
            object.draw(screen)

    def set_level(self, level_name):
        self.level = self.level_manager.get_level(level_name)

    def add_player(self, player_car):
        player_car.x = 960
        player_car.y = 540
        self.players[player_car.player_name] = player_car
        self.components.append(player_car)

    def clear_race(self):
        self.components = [
            component for component in self.components if not isinstance(component, Car)
        ]
        self.players = {}
