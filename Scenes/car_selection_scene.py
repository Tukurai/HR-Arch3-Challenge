import copy
import pygame
from Engine.player_car import PlayerCar
from Enums.direction import Direction
from Scenes.game_scene import GameScene
from Settings import settings
from Settings.user_events import BUTTON_CLICK


class CarSelectionScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Car selection", components)
        self.car_selection = self.get_car_selection()
        self.selected_cars = []
        self.cars_needed = 1
        self.player_name = ""
        self.car_buttons = []

    def handle_event(self, event):
        if event.type == BUTTON_CLICK:
            self.car_buttons.append(event.button)

            if event.button.component_name in self.car_selection:
                car = copy.copy(self.car_selection[event.button.component_name])
                car.player_name = f"Player_{len(self.selected_cars)+1}"
                car.set_controls(
                    CarSelectionScene.get_key_mapping(len(self.selected_cars) + 1)
                )
                self.selected_cars.append(car)
                event.button.selected = True

                if len(self.selected_cars) >= self.cars_needed:
                    race_scene = self.scene_manager.get_scene_by_name("Race")
                    race_scene.clear_race()
                    race_scene.add_players(self.selected_cars)

                    self.scene_manager.set_active_scene(race_scene)

            elif event.button.component_name == "BackButton":
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("Main menu")
                )

            if settings.DEBUG_MODE:
                print(f"Button {event.button.component_name} clicked!")

        return super().handle_event(event)

    def scene_changed(self):
        return super().scene_changed()

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
            "car1": PlayerCar(
                "Player1",
                None,
                180,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_black_small_1.png"),
                1.10,
                30,
            ),
            "car2": PlayerCar(
                "Player2",
                None,
                240,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_red_small_1.png"),
                1.10,
                25,
            ),
            "car3": PlayerCar(
                "Player3",
                None,
                220,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_yellow_small_1.png"),
                1.10,
                27,
            ),
            "car4": PlayerCar(
                "Player4",
                None,
                160,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_green_small_1.png"),
                1.10,
                35,
            ),
            "car5": PlayerCar(
                "Player5",
                None,
                280,
                1.0,
                "Player Car",
                self.scene_manager.sprite_manager.get_car("car_blue_small_1.png"),
                1.10,
                20,
            ),
        }
