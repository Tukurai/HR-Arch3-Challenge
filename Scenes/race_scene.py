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
        self.players = []

        self.set_level("map_right")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("High score")
                )
            elif event.key == pygame.K_1:
                self.change_level("map_right")
            elif event.key == pygame.K_2:
                self.change_level("map_down")
            elif event.key == pygame.K_3:
                self.change_level("map_left")
            elif event.key == pygame.K_4:
                self.change_level("map_up")
            elif event.key == pygame.K_5:
                self.change_level("map_complex")

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

    def change_level(self, level_name):
        '''Change the level internally and update the players to the new level.'''
        cached_players = self.players
        self.clear_race()
        self.set_level(level_name)
        self.add_players(cached_players)


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
        debug_pointer = Component(
            "Debug pointer", None, (x - 5, y - 5), 10, 10, 0, 1.00, color=(255, 0, 0)
        )
        direction = self.get_direction(starting_position, first_checkpoint)

        match direction:
            case Direction.UP:
                y += 40 * settings.GAME_SCALE
            case Direction.DOWN:
                y -= 40 * settings.GAME_SCALE
            case Direction.LEFT:
                x += 40 * settings.GAME_SCALE
            case Direction.RIGHT:
                x -= 40 * settings.GAME_SCALE

        # update all players, set rotation based on direction, 0 up, 90 right, 180 down, 270 left
        for player in self.players:
            player.rotation = direction.value * 90

        # set starting positions
        for index in range(6):
            # Your code here
            pair_index = index % 2
            row_index = index // 2
            pair_offset = 50 * settings.GAME_SCALE * settings.CAR_SCALE
            row_offset = 140 * settings.GAME_SCALE * settings.CAR_SCALE
            debug_car_pointer = copy.copy(debug_pointer)
            debug_x = 0
            debug_y = 0

            if direction in (Direction.UP, Direction.DOWN):
                if pair_index == 0:
                    debug_x = -pair_offset
                else:
                    debug_x = pair_offset
                if direction == Direction.UP:
                    debug_y = row_offset * row_index
                else:
                    debug_y = -row_offset * row_index
            else:  # Direction.LEFT, Direction.RIGHT
                if direction == Direction.LEFT:
                    debug_x = row_offset * row_index
                else:
                    debug_x = -row_offset * row_index
                if pair_index == 0:
                    debug_y = pair_offset
                else:
                    debug_y = -pair_offset

            debug_car_pointer.x = x + debug_x - 5
            debug_car_pointer.y = y + debug_y - 5
            # self.components.append(debug_car_pointer) # Uncomment to see debug pointers

            if len(self.players) >= index + 1:
                car = self.players[index]
                match direction: # Set the car position based on the direction (fuck magic numbers)
                    case Direction.UP:
                        car.x = debug_car_pointer.x + 13 - (car.get_scaled_height() / 2)
                        car.y = debug_car_pointer.y - 13 - (car.get_scaled_width() / 2)
                    case Direction.DOWN:
                        car.x = debug_car_pointer.x + 13 - (car.get_scaled_height() / 2)
                        car.y = debug_car_pointer.y - 13 - (car.get_scaled_width() / 2)  
                    case Direction.LEFT:
                        car.x = debug_car_pointer.x + 8 - (car.get_scaled_width() / 2)
                        car.y = debug_car_pointer.y + 13 - (car.get_scaled_height() / 2)
                    case Direction.RIGHT:
                        car.x = debug_car_pointer.x - 13 - (car.get_scaled_width() / 2)
                        car.y = debug_car_pointer.y + 13 - (car.get_scaled_height() / 2)

    def get_direction(self, checkpoint_a, checkpoint_b):
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

    def add_players(self, players):
        self.players += players
        self.components += players

        self.set_starting_positions(
            self.level["Checkpoints"][0], self.level["Checkpoints"][1]
        )

    def clear_race(self):
        self.components = [
            component for component in self.components if not isinstance(component, Car)
        ]
        self.players = []
