import copy

import pygame
from Engine.component import Component
from Enums.direction import Direction
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
            "Objects": self.get_level_layer(level, "Objects"),
            "Checkpoints": self.get_level_checkpoints(level, "Checkpoints"),
        }

    def set_starting_positions(self, starting_position, first_checkpoint):
        scaled_tile_size = settings.TILE_SIZE * settings.GAME_SCALE
        x = (
            (starting_position[0] * scaled_tile_size)
            + settings.TRACK_OFFSET
            + (scaled_tile_size / 2)
        )
        y = (
            (starting_position[1] * scaled_tile_size)
            + settings.TRACK_OFFSET
            + (scaled_tile_size / 2)
        )

        direction = self.get_direction(starting_position, first_checkpoint)
        
        # update all players, set rotation based on direction, 0 up, 90 right, 180 down, 270 left  
        for player in self.players.values():  
            player.rotation = direction.value * 90  # assuming Direction.UP == 0, RIGHT == 1, DOWN == 2, LEFT == 3  

        # TODO: make it put the cars on track 2 by 2.
        for i, player in enumerate(self.players.values()):  
            if direction in (Direction.UP, Direction.DOWN):  
                offset_x = (i % 2) * scaled_tile_size / 2  
                offset_y = (i // 2) * scaled_tile_size / 8  
            else:  # Direction.LEFT, Direction.RIGHT  
                offset_x = (i // 2) * scaled_tile_size / 8  
                offset_y = (i % 2) * scaled_tile_size / 2  
            
            player.x = x + offset_x  
            player.y = y + offset_y  

    def get_direction(self,checkpoint_a, checkpoint_b):
        x1, y1 = checkpoint_a
        x2, y2 = checkpoint_b

        if x1 < x2:
            return Direction.RIGHT
        elif x1 > x2:
            return Direction.LEFT
        elif y1 < y2:
            return Direction.DOWN
        elif y1 > y2:
            return Direction.UP

    def get_level_layer(self, level, layer_name):
        layer = []

        row_index = 0
        for tilerow in level[layer_name]:
            column_index = 0
            for tile in tilerow:
                if tile is not None:
                    # This shallow copy resolves the issue of setting different x/y settings on the same object
                    tile = copy.copy(tile)
                    tile.x = (
                        settings.TILE_SIZE * settings.GAME_SCALE * column_index
                    ) + settings.TRACK_OFFSET
                    tile.y = (
                        settings.TILE_SIZE * settings.GAME_SCALE * row_index
                    ) + settings.TRACK_OFFSET
                    layer.append(tile)
                column_index += 1
            row_index += 1
            column_index = 0

        return layer

    def get_level_checkpoints(self, level, layer_name):
        checkpoints = {}

        row_index = 0
        for tilerow in level[layer_name]:
            column_index = 0
            for tile in tilerow:
                if tile is not None and tile != -1:
                    checkpoints[tile] = (column_index, row_index)
                column_index += 1
            row_index += 1
            column_index = 0

        return {k: checkpoints[k] for k in sorted(checkpoints)}

    def add_player(self, player_car):
        player_car.x = 960
        player_car.y = 540
        self.players[player_car.player_name] = player_car
        self.components.append(player_car)
        
        self.set_starting_positions(
            self.level["Checkpoints"][0], self.level["Checkpoints"][1]
        )

    def clear_race(self):
        self.components = [
            component for component in self.components if not isinstance(component, Car)
        ]
        self.players = {}
