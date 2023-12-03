import copy
import math
import time

import pygame
from Engine.component import Component
from Engine.player_car import PlayerCar
from Enums.direction import Direction
from Manager.collision_manager import CollisionManager
from Manager.level_manager import LevelManager
from Engine.car import Car
from Scenes.game_scene import GameScene
from Settings import settings
from Settings.user_events import RESET_CAR_EVENT, BUTTON_CLICK, START_RACE_EVENT, SUBMIT_SCORE_EVENT


class RaceScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Race", components)
        self.level_manager = LevelManager(sprite_manager)
        self.collision_manager = CollisionManager(scene_manager, self)
        self.players = []
        self.start_time = time.time()
        self.level_name = ""

        self.set_level("map_right")

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.change_level("map_right")
            elif event.key == pygame.K_2:
                self.change_level("map_down")
            elif event.key == pygame.K_3:
                self.change_level("map_left")
            elif event.key == pygame.K_4:
                self.change_level("map_up")
            elif event.key == pygame.K_5:
                self.change_level("map_complex")
        elif event.type == RESET_CAR_EVENT:
            self.reset_car_to_checkpoint(event.car)

        if event.type == BUTTON_CLICK:
            if event.button.component_name == "EndRaceButton":
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("High score")
                )

        for component in self.components:  # Ignoring level objs.
            component.handle_event(event)

        return super().handle_event(event)

    def update(self, timedelta, input_state):
        for component in self.components:
            component.update(timedelta, input_state)

        for car in self.players:
            self.update_checkpoints(car)
            if not isinstance(car, PlayerCar):
                self.drive_car(car)

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

        if settings.DEBUG_MODE:
            self.draw_checkpoints(screen)

    def change_level(self, level_name):
        """Change the level internally and update the players to the new level."""
        cached_players = self.players
        for player in cached_players:
            player.reset()

        self.clear_race()
        self.set_level(level_name)
        self.add_players(cached_players)
        for player in cached_players:
            if isinstance(player, PlayerCar):
                start_race_event = pygame.event.Event(
                    START_RACE_EVENT,
                    name=player.player_name,
                    level_name=self.level_name,
                )
                pygame.event.post(start_race_event)

    def set_level(self, level_name):
        level = self.level_manager.get_level(level_name)
        self.level_name = level_name

        self.level = {
            "Ground": self.get_level_layer(level, "Ground"),
            "Roads": self.get_level_layer(level, "Roads"),
            "Objects": self.get_level_layer(level, "Objects"),
            "Checkpoints": self.get_level_checkpoints(level, "Checkpoints"),
        }

    def drive_car(self, car):
        direction = self.get_direction(
            self.level["Checkpoints"][car.current_checkpoint],
            self.level["Checkpoints"][car.next_checkpoint],
        )
        ideal_rotation = direction.value * 90

        next_next_checkpoint = self.get_next_checkpoint(car.next_checkpoint)
        next_next_direction = self.get_direction(
            self.level["Checkpoints"][car.next_checkpoint],
            self.level["Checkpoints"][next_next_checkpoint],
        )

        # Determine the center of the checkpoint, or the ideal turning point, this requires me to know the next checkpoint.
        scaled_tile_size = settings.TILE_SIZE * settings.GAME_SCALE
        small_offset = scaled_tile_size * 0.47
        large_offset = scaled_tile_size * 0.53
        center_offset = scaled_tile_size * 0.5
        target_pos_offset = (0, 0)
        match direction:
            case Direction.UP:
                match next_next_direction:
                    case Direction.RIGHT:
                        target_pos_offset = (large_offset, large_offset)
                    case Direction.LEFT:
                        target_pos_offset = (small_offset, large_offset)
                    case Direction.UP:
                        target_pos_offset = (center_offset, center_offset)
            case Direction.DOWN:
                match next_next_direction:
                    case Direction.RIGHT:
                        target_pos_offset = (large_offset, small_offset)
                    case Direction.LEFT:
                        target_pos_offset = (small_offset, small_offset)
                    case Direction.DOWN:
                        target_pos_offset = (center_offset, center_offset)
            case Direction.LEFT:
                match next_next_direction:
                    case Direction.UP:
                        target_pos_offset = (large_offset, small_offset)
                    case Direction.DOWN:
                        target_pos_offset = (large_offset, large_offset)
                    case Direction.LEFT:
                        target_pos_offset = (center_offset, center_offset)
            case Direction.RIGHT:
                match next_next_direction:
                    case Direction.UP:
                        target_pos_offset = (small_offset, small_offset)
                    case Direction.DOWN:
                        target_pos_offset = (small_offset, large_offset)
                    case Direction.RIGHT:
                        target_pos_offset = (center_offset, center_offset)

        x = (
            (self.level["Checkpoints"][car.next_checkpoint][0] * scaled_tile_size)
            + settings.TRACK_OFFSET
            + target_pos_offset[0]
        )
        y = (
            (self.level["Checkpoints"][car.next_checkpoint][1] * scaled_tile_size)
            + settings.TRACK_OFFSET
            + target_pos_offset[1]
        )

        ideal_rotation = self.calculate_rotation(car.x, car.y, x, y)
        rotation_difference = self.fastest_rotation_direction(
            car.rotation, ideal_rotation
        )

        turning = False
        if rotation_difference > 3:
            car.handle_controls(Direction.RIGHT)
            turning = True
        elif rotation_difference < -3:
            car.handle_controls(Direction.LEFT)
            turning = True

        if (
            abs(car.x - x) <= scaled_tile_size
            and abs(car.y - y) <= scaled_tile_size
            and turning
        ):
            if car.current_speed > 100:
                car.handle_controls(Direction.DOWN)
            elif car.current_speed > 75:
                car.apply_drag()
            else:
                car.handle_controls(Direction.UP)
        else:
            car.handle_controls(Direction.UP)

    def calculate_rotation(self, current_x, current_y, target_x, target_y):
        dx = target_x - current_x
        dy = target_y - current_y
        radians = math.atan2(dy, dx)
        degrees = math.degrees(radians)
        adjusted_degrees = (90 + degrees) % 360
        return adjusted_degrees

    def fastest_rotation_direction(self, current_rotation, target_rotation):
        difference = (target_rotation - current_rotation) % 360
        if difference > 180:
            difference -= 360
        return difference

    def set_starting_positions(self, starting_position, first_checkpoint):
        scaled_tile_size = settings.TILE_SIZE * settings.GAME_SCALE
        max_players = settings.MAX_PLAYERS

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

        while len(self.players) < max_players:
            ai_car = Car(
                180,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_black_small_1.png"),
                1.10,
            )
            self.players.append(ai_car)
            self.components.append(ai_car)

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
        for index in range(max_players):
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
                # Set the car position based on the direction (fuck magic numbers)
                match direction:
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
        self.start_time = time.time()

    def reset_car_to_checkpoint(self, car):
        checkpoint = self.get_checkpoint_component(
            self.level["Checkpoints"][car.current_checkpoint]
        )

        rotation = self.get_direction(
            self.level["Checkpoints"][car.current_checkpoint],
            self.level["Checkpoints"][car.next_checkpoint],
        )

        offset_x = 0
        offset_y = 0
        match rotation:
            case Direction.UP:
                offset_x = -10
                offset_y = -32
            case Direction.DOWN:
                offset_x = -10
                offset_y = 0
            case Direction.LEFT:
                offset_x = -32
                offset_y = -10
            case Direction.RIGHT:
                offset_x = -2
                offset_y = -10

        car.x = checkpoint.x + offset_x + checkpoint.width / 2
        car.y = checkpoint.y + offset_y + checkpoint.height / 2
        car.rotation = rotation.value * 90

    def get_next_checkpoint(self, current_checkpoint):
        next_checkpoint = current_checkpoint + 1
        if next_checkpoint >= len(self.level["Checkpoints"]):
            next_checkpoint = 0
        return next_checkpoint

    def update_checkpoints(self, car):
        mask_car = pygame.mask.from_surface(
            car.get_scaled_rotated_sprite_or_mask(car.mask_layers[0])[0]
        )

        checkpoint = self.get_checkpoint_component(
            self.level["Checkpoints"][car.next_checkpoint]
        )
        mask_checkpoint = pygame.mask.from_surface(checkpoint.sprite)

        if mask_checkpoint.overlap(
            mask_car, (car.x - checkpoint.x, car.y - checkpoint.y)
        ):
            car.current_checkpoint = car.next_checkpoint
            car.next_checkpoint = self.get_next_checkpoint(car.current_checkpoint)

            if car.current_checkpoint == 0:
                car.lap += 1
                if car.lap == 3:
                    # get all players that are an instance of playercar
                    player_cars = [
                        player
                        for player in self.players
                        if isinstance(player, PlayerCar)
                    ]
                    if isinstance(car, PlayerCar):
                        car.caclulate_score(self.start_time, time.time())

                    progress_to_next_scene = True
                    for player in player_cars:
                        if player.lap < 3:
                            progress_to_next_scene = False

                    if progress_to_next_scene:
                        for player in player_cars:
                            submit_score_event = pygame.event.Event(
                                SUBMIT_SCORE_EVENT,
                                name=player.player_name,
                                score=player.score,
                                level_name=self.level_name,
                            )
                            pygame.event.post(submit_score_event)

                        self.scene_manager.set_active_scene(
                            self.scene_manager.get_scene_by_name("High score")
                        )

    def get_checkpoint_component(self, checkpoint):
        scaled_tile_size = settings.TILE_SIZE * settings.GAME_SCALE
        x = (
            (checkpoint[0] * scaled_tile_size)
            + settings.TRACK_OFFSET
            + (scaled_tile_size / 2)
        )
        y = (
            (checkpoint[1] * scaled_tile_size)
            + settings.TRACK_OFFSET
            + (scaled_tile_size / 2)
        )

        debug_pointer = Component(
            "Debug pointer", None, (x - 5, y - 5), 10, 10, 0, 1.00, color=(255, 0, 0)
        )

        checkpoint_component = Component(
            "Debug pointer",
            None,
            (x - scaled_tile_size / 2, y - scaled_tile_size / 2),
            scaled_tile_size,
            scaled_tile_size,
            0,
            1.00,
            color=(255, 255, 255),
        )
        return checkpoint_component

    def get_checkpoint_debug_component(self, checkpoint):
        scaled_tile_size = settings.TILE_SIZE * settings.GAME_SCALE
        x = (
            (checkpoint[0] * scaled_tile_size)
            + settings.TRACK_OFFSET
            + (scaled_tile_size / 2)
        )
        y = (
            (checkpoint[1] * scaled_tile_size)
            + settings.TRACK_OFFSET
            + (scaled_tile_size / 2)
        )

        debug_pointer = Component(
            "Debug pointer", None, (x - 5, y - 5), 10, 10, 0, 1.00, color=(255, 0, 0)
        )
        return debug_pointer

    def draw_checkpoints(self, screen):
        for checkpoint in self.level["Checkpoints"].values():
            self.get_checkpoint_debug_component(checkpoint).draw(screen)
            # self.get_checkpoint_component(checkpoint).draw(screen)
