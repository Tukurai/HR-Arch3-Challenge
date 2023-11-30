import math

import pygame
from Engine.car import Car
from Enums.direction import Direction


class PlayerCar(Car):
    def __init__(
        self,
        player_name,
        controls,
        max_speed,
        drag,
        component_name,
        full_sprite,
        x,
        y,
        rotation,
        depth,
    ):
        super().__init__(
            max_speed, drag, component_name, full_sprite, x, y, rotation, depth
        )
        self.player_name = player_name
        self.controls = controls
        self.reverse_controls = None
        if controls is not None:
            self.set_controls(controls)
    
    def set_controls(self, controls):
        self.controls = controls
        self.reverse_controls = {v: k for k, v in controls.items()}

    def handle_event(self, event):
        pass

    def update(self, timedelta, input_state):
        keys = input_state.cur_keyboard_state

        if keys[self.reverse_controls[Direction.UP]]:
            self.handle_controls(Direction.UP)
        elif keys[self.reverse_controls[Direction.DOWN]]:
            self.handle_controls(Direction.DOWN)
        else:
            self.apply_drag()

        if keys[self.reverse_controls[Direction.LEFT]]:
            self.handle_controls(Direction.LEFT)
        elif keys[self.reverse_controls[Direction.RIGHT]]:
            self.handle_controls(Direction.RIGHT)