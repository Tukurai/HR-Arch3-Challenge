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
        component_name,
        full_sprite,
        x,
        y,
        rotation,
        depth,
    ):
        super().__init__(
            max_speed, component_name, full_sprite, x, y, rotation, depth
        )
        self.player_name = player_name
        self.controls = controls
        self.reverse_controls = {v: k for k, v in controls.items()}  

    def handle_event(self, event):
        pass

    def update(self, timedelta, input_state):
        keys = input_state.cur_keyboard_state

        if keys[self.reverse_controls[Direction.UP]]:  
            self.handle_controls(Direction.UP)  
        if keys[self.reverse_controls[Direction.DOWN]]:  
            self.handle_controls(Direction.DOWN)  
        if keys[self.reverse_controls[Direction.LEFT]]:  
            self.handle_controls(Direction.LEFT)  
        if keys[self.reverse_controls[Direction.RIGHT]]:  
            self.handle_controls(Direction.RIGHT)  

        self.move(timedelta)

    def draw(self, screen):
        # Create a new surface with the car image, rotated
        rotated_car = pygame.transform.rotate(self.sprite, -self.rotation)

        # Calculate the new upper left corner position of the rotated car
        rect = rotated_car.get_rect(
            center=self.sprite.get_rect(topleft=(self.x, self.y)).center
        )

        # Draw the rotated car onto the window
        screen.blit(rotated_car, rect.topleft)

    def handle_controls(self, direction):
        match (direction):
            case Direction.UP:
                self.current_speed = self.speed_limiter(self.current_speed + 3)
            case Direction.DOWN:
                self.current_speed = self.speed_limiter(self.current_speed - 2)
            case Direction.LEFT:
                self.rotation = (
                    self.rotation - 2
                ) % 360  # Rotate 5 degrees to the left
            case Direction.RIGHT:
                self.rotation = (
                    self.rotation + 2
                ) % 360  # Rotate 5 degrees to the right

    def speed_limiter(self, speed):
        return min(self.max_speed, max(-(self.max_speed / 2), speed))

    def move(self, timedelta):  # Override the default with player controls.
        # Calculate the new x and y position based on the rotation.
        # In this case, we're assuming that a rotation of 0 means the car is facing up
        # (negative y direction), and rotations are in degrees.

        # Convert rotation to radians for math functions
        rad = math.radians(self.rotation)

        dx = self.current_speed * math.sin(rad) * timedelta
        dy = -self.current_speed * math.cos(rad) * timedelta

        # Update the position
        # TODO: Handle collision before we set the actual X and Y
        self.x += dx
        self.y += dy
