import copy

import pygame
from Engine.component import Component
from Manager.collision_manager import CollisionManager
from Manager.level_manager import LevelManager
from Engine.car import Car
from Scenes.game_scene import GameScene
from Settings import settings


class RaceScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Race", components)
        self.level_manager = LevelManager(sprite_manager)
        self.collision_manager = CollisionManager(scene_manager, self)
        self.players = {}

        self.set_level("testmap_checkpoints")

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
            
        self.collision_manager.update(timedelta, input_state)

    def draw(self, screen):
        for tile in self.level["Ground"]:
            tile.draw(screen)

        for tile in self.level["Roads"]:
            tile.draw(screen)

        for tile in self.level["Objects"]:
            tile.draw(screen)

        for component in self.components:
            component.draw(screen)

    def set_level(self, level_name):
        level = self.level_manager.get_level(level_name)
        
        self.level = {
            "Ground": self.get_level_layer(level, "Ground"),
            "Roads": self.get_level_layer(level, "Roads"),
            "Objects" : self.get_level_layer(level, "Objects"),
            "Checkpoints" : self.get_level_checkpoints(level, "Checkpoints")
        }

    def get_level_layer(self, level, layer_name):
        layer = []

        row_index = 0
        for tilerow in level[layer_name]:
            column_index = 0
            for tile in tilerow:
                if tile is not None:
                    # TODO This shallow copy resolves the issue of setting different x/y settings on the same object but I'm not sure this is how we want to do it
                    tile = copy.copy(tile)
                    tile.x = (settings.TILE_SIZE * settings.GAME_SCALE * column_index) + settings.TRACK_OFFSET
                    tile.y = (settings.TILE_SIZE * settings.GAME_SCALE * row_index)+ settings.TRACK_OFFSET
                    layer.append(tile)
                column_index += 1
            row_index += 1
            column_index = 0

        return layer
    
    def get_level_checkpoints(self, level, layer_name):
        checkpoints = []

        row_index = 0
        for tilerow in level[layer_name]:
            column_index = 0
            for tile in tilerow:
                if tile is not None:
                    checkpoints.append((column_index, row_index))
                column_index += 1
            row_index += 1
            column_index = 0

        return checkpoints

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
