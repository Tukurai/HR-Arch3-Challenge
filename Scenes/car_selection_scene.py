import copy
from Engine.button_component import ButtonComponent
import pygame
from Engine.player_car import PlayerCar
from Engine.text_box import TextBox
from Engine.text_component import TextComponent
from Enums.direction import Direction
from Scenes.game_scene import GameScene
from Settings import settings
from Settings.user_events import BUTTON_CLICK, TEXT_BOX_INPUT


class CarSelectionScene(GameScene):
    def __init__(self, scene_manager, sprite_manager, components):
        super().__init__(scene_manager, sprite_manager, "Car selection", components)
        self.car_selection = self.get_car_selection()
        self.selected_cars = []
        self.cars_needed = 1
        self.player_name = ""
        self.car_buttons = []

    def handle_event(self, event):

        if event.type == TEXT_BOX_INPUT:
            self.player_name = event.player_name
            print("GETTING NAME IN CAR SELECTION SCENE")
        if event.type == BUTTON_CLICK:
            self.car_buttons.append(event.button)

            if event.button.component_name in self.car_selection:
                car = copy.copy(self.car_selection[event.button.component_name])
                car.player_name = f"Player_{len(self.selected_cars)+1}"
                car.component_name = self.player_name
                car.set_controls(
                    CarSelectionScene.get_key_mapping(len(self.selected_cars) + 1))
                self.selected_cars.append(car)
                event.button.selected = True

                if len(self.selected_cars) >= self.cars_needed:
                    race_scene = self.scene_manager.get_scene_by_name("Race")
                    race_scene.clear_race()
                    race_scene.add_players(self.selected_cars)

                    self.scene_manager.set_active_scene(race_scene)

            elif event.button.component_name == "BackButton":
                self.scene_manager.set_active_scene(
                    self.scene_manager.get_scene_by_name("Main menu"))

            if settings.DEBUG_MODE:
                print(f"Button {event.button.component_name} clicked!")

        return super().handle_event(event)

    def build_ui(self):
        screen = self.scene_manager.screen

        self.components.extend(
            [
                TextComponent(
                    "Header",
                    "Select a car",
                    36,
                    True,
                    None,
                    (screen.get_width() / 2, 200),
                    0,
                    0,
                    0,
                    1.00,
                ),
                TextComponent(
                    "Instruction",
                    "Enter your name, hit enter and select a car",
                    24,
                    True,
                    None,
                    (screen.get_width() / 2, screen.get_height() - 200),
                    0,
                    0,
                    0,
                    1.00,
                ),
                ButtonComponent(
                    "BackButton",
                    self.sprite_manager.get_full_ui_element(
                        "blue_button00.png",
                        "green_button00.png",
                        "green_button01.png",
                    ),
                    (
                        screen.get_width()
                        - self.sprite_manager.get_ui_element("blue_button00.png").width
                        - 220,
                        self.scene_manager.screen.get_height()
                        - self.sprite_manager.get_ui_element("blue_button00.png").height
                        - 150,
                    ),
                    0,
                    1,
                    "Back to main menu",
                    24,
                    True,
                ),
                TextBox(
                    "NameTextBox",
                    (
                        screen.get_width() / 2 - 95,
                        screen.get_height() / 2 - 255,
                    ),
                    190,
                    49,
                    text="Enter your name",
                    font_size=32,
                    saved_text_display=TextComponent(
                        "PlayerName",
                        "Player Name: ",
                        24,
                        True,
                        None,
                        (
                            screen.get_width() / 2,
                            (screen.get_height() / 2) - 185,
                        ),
                        0,
                        0,
                        0,
                        1.00,
                    ),
                ),
                ButtonComponent(
                    "car1",
                    self.sprite_manager.get_full_car_ui_element(
                        "car_black_small_1.png"
                    ),
                    (
                        (screen.get_width() / 2)
                        - (
                            self.sprite_manager.get_car("car_black_small_1.png").width
                            / 2
                        )
                        - 200,
                        screen.get_height() / 2,
                    ),
                    0,
                    1.00,
                    "",
                    1,
                    True,
                ),
                ButtonComponent(
                    "car2",
                    self.sprite_manager.get_full_car_ui_element("car_red_small_1.png"),
                    (
                        (screen.get_width() / 2)
                        - (self.sprite_manager.get_car("car_red_small_1.png").width / 2)
                        - 100,
                        screen.get_height() / 2,
                    ),
                    0,
                    1.00,
                    "",
                    1,
                    True,
                ),
                ButtonComponent(
                    "car3",
                    self.sprite_manager.get_full_car_ui_element(
                        "car_yellow_small_1.png"
                    ),
                    (
                        (screen.get_width() / 2)
                        - (
                            self.sprite_manager.get_car("car_yellow_small_1.png").width
                            / 2
                        ),
                        screen.get_height() / 2,
                    ),
                    0,
                    1.00,
                    "",
                    1,
                    True,
                ),
                ButtonComponent(
                    "car4",
                    self.sprite_manager.get_full_car_ui_element(
                        "car_green_small_1.png"
                    ),
                    (
                        (screen.get_width() / 2)
                        - (
                            self.sprite_manager.get_car("car_green_small_1.png").width
                            / 2
                        )
                        + 100,
                        screen.get_height() / 2,
                    ),
                    0,
                    1.00,
                    "",
                    1,
                    True,
                ),
                ButtonComponent(
                    "car5",
                    self.sprite_manager.get_full_car_ui_element("car_blue_small_1.png"),
                    (
                        (screen.get_width() / 2)
                        - (
                            self.sprite_manager.get_car("car_blue_small_1.png").width
                            / 2
                        )
                        + 200,
                        screen.get_height() / 2,
                    ),
                    0,
                    1.00,
                    "",
                    1,
                    True,
                ),
            ]
        )

    def set_cars_needed(self, cars_needed):
        self.cars_needed = cars_needed
        self.components = []
        self.build_ui()

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
