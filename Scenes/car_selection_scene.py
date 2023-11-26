import pygame
from Engine.player_car import PlayerCar
from Enums.direction import Direction
from Scenes.game_scene import GameScene


class CarSelectionScene(GameScene):
    def __init__(self, scene_manager, components):
        super().__init__(scene_manager, "Car selection", components)
        self.car_selection = self.get_car_selection()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.car_selection:
                car = self.car_selection[event.key]

                race_scene = self.scene_manager.get_scene_by_name("Race")
                race_scene.clear_race()
                race_scene.add_player(car)

                self.scene_manager.set_active_scene(race_scene)

        return super().handle_event(event)

    def get_car_selection(self):
        return {
            pygame.K_1: PlayerCar(
                "Player",
                {
                    pygame.K_w: Direction.UP,
                    pygame.K_a: Direction.LEFT,
                    pygame.K_s: Direction.DOWN,
                    pygame.K_d: Direction.RIGHT,
                },
                180,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.game_object_library["Cars"]["car_black_1.png"],
                0,
                0,
                0,
                1.10,
            ),
            pygame.K_2: PlayerCar(
                "Player",
                {
                    pygame.K_w: Direction.UP,
                    pygame.K_a: Direction.LEFT,
                    pygame.K_s: Direction.DOWN,
                    pygame.K_d: Direction.RIGHT,
                },
                240,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.game_object_library["Cars"]["car_red_1.png"],
                0,
                0,
                0,
                1.10,
            ),
            pygame.K_3: PlayerCar(
                "Player",
                {
                    pygame.K_w: Direction.UP,
                    pygame.K_a: Direction.LEFT,
                    pygame.K_s: Direction.DOWN,
                    pygame.K_d: Direction.RIGHT,
                },
                220,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.game_object_library["Cars"]["car_yellow_1.png"],
                0,
                0,
                0,
                1.10,
            ),
            pygame.K_4: PlayerCar(
                "Player",
                {
                    pygame.K_w: Direction.UP,
                    pygame.K_a: Direction.LEFT,
                    pygame.K_s: Direction.DOWN,
                    pygame.K_d: Direction.RIGHT,
                },
                160,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.game_object_library["Cars"]["car_green_1.png"],
                0,
                0,
                0,
                1.10,
            ),
            pygame.K_5: PlayerCar(
                "Player",
                {
                    pygame.K_w: Direction.UP,
                    pygame.K_a: Direction.LEFT,
                    pygame.K_s: Direction.DOWN,
                    pygame.K_d: Direction.RIGHT,
                },
                280,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.game_object_library["Cars"]["car_blue_1.png"],
                0,
                0,
                0,
                1.10,
            ),
        }
