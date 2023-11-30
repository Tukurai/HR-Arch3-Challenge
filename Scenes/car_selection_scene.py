import pygame
from Engine.player_car import PlayerCar
from Enums.direction import Direction
from Scenes.game_scene import GameScene


class CarSelectionScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Car selection", components)
        self.car_selection = self.get_car_selection()
        self.selected_cars = []
        self.cars_needed = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.car_selection:
                car = self.car_selection[event.key]
                car.player_name = f"Player_{len(self.selected_cars)+1}"
                car.set_controls(CarSelectionScene.get_key_mapping(len(self.selected_cars)+1))
                self.selected_cars.append(car)

                if len(self.selected_cars) >= self.cars_needed:
                    race_scene = self.scene_manager.get_scene_by_name("Race")
                    race_scene.clear_race()
                    race_scene.add_players(self.selected_cars)                

                    self.scene_manager.set_active_scene(race_scene)

        return super().handle_event(event)
    
    def get_key_mapping(number):
        match number:
            case 1:
                return {
                    pygame.K_w: Direction.UP,
                    pygame.K_a: Direction.LEFT,
                    pygame.K_s: Direction.DOWN,
                    pygame.K_d: Direction.RIGHT,
                }
            case 2:
                return {
                    pygame.K_UP: Direction.UP,
                    pygame.K_LEFT: Direction.LEFT,
                    pygame.K_DOWN: Direction.DOWN,
                    pygame.K_RIGHT: Direction.RIGHT,
                }
        return None

    def get_car_selection(self):
        return {
            pygame.K_1: PlayerCar(
                "Player",
                None,
                180,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_black_small_1.png"),
                1.10,
            ),
            pygame.K_2: PlayerCar(
                "Player",
                None,
                240,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_red_small_1.png"),
                1.10,
            ),
            pygame.K_3: PlayerCar(
                "Player",
                None,
                220,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_yellow_small_1.png"),
                1.10,
            ),
            pygame.K_4: PlayerCar(
                "Player",
                None,
                160,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_green_small_1.png"),
                1.10,
            ),
            pygame.K_5: PlayerCar(
                "Player",
                None,
                280,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_blue_small_1.png"),
                1.10,
            ),
        }
