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
        self.collision_manager = CollisionManager(scene_manager)
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
        empty_tile = Component("Empty tile",None,0,0,128,128,0,0.3,(40,40,40))

        row_index = 0
        for tilerow in self.level["Ground"]:
            column_index = 0
            for tile in tilerow:
                if tile is not None:
                    tile.draw(
                        screen,
                        (settings.TILE_SIZE * settings.GAME_SCALE * column_index)
                        + settings.TRACK_OFFSET,
                        (settings.TILE_SIZE * settings.GAME_SCALE * row_index)
                        + settings.TRACK_OFFSET,
                    )
                column_index += 1
            row_index += 1
            column_index = 0
        row_index = 0

        for tilerow in self.level["Roads"]:
            column_index = 0
            for tile in tilerow:
                if tile is not None:
                    tile.draw(
                        screen,
                        (settings.TILE_SIZE * settings.GAME_SCALE * column_index)
                        + settings.TRACK_OFFSET,
                        (settings.TILE_SIZE * settings.GAME_SCALE * row_index)
                        + settings.TRACK_OFFSET,
                    )
                column_index += 1
            row_index += 1
            column_index = 0
        row_index = 0

        row_index = 0
        for tilerow in self.level["Objects"]:
            column_index = 0
            for object in tilerow:
                if object is not None:
                    object.draw(
                        screen,
                        (settings.TILE_SIZE * settings.GAME_SCALE * column_index)
                        + settings.TRACK_OFFSET,
                        (settings.TILE_SIZE * settings.GAME_SCALE * row_index)
                        + settings.TRACK_OFFSET,
                    )
                column_index += 1
            row_index += 1
            column_index = 0
        row_index = 0

        for component in self.components:
            component.draw(screen)

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
