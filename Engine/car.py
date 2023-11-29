import datetime
import math
import pygame
from Engine.component import Component
from Enums.direction import Direction
from Settings import settings


class Car(Component):
    def __init__(
        self, max_speed, drag, component_name, full_sprite, x, y, rotation, depth
    ):
        super().__init__(
            component_name,
            full_sprite.sprite,
            x,
            y,
            full_sprite.width,
            full_sprite.height,
            rotation,
            depth,
            scale=settings.CAR_SCALE,
            mask_layers=full_sprite.mask_layers,
        )
        self.max_speed = max_speed
        self.current_speed = 0
        self.drag = drag
        self.prev_x = x
        self.prev_y = y

    def handle_event(self, event):
        pass

    def update(self, timedelta, input_state):
        self.apply_drag()  # Only do this if the car is not actively moving backward of forward.

        self.move(timedelta)

    def draw(self, screen):
        super().draw(screen, rotation=-self.rotation, scale=self.scale)

    def handle_controls(self, direction):
        match (direction):
            case Direction.UP:
                self.current_speed = self.speed_limiter(self.current_speed + 3)
            case Direction.DOWN:
                self.current_speed = self.speed_limiter(self.current_speed - 2)
            case Direction.LEFT:
                if self.current_speed != 0:
                    self.rotation = (
                        self.rotation - 2
                    ) % 360  # Rotate 5 degrees to the left
            case Direction.RIGHT:
                if self.current_speed != 0:
                    self.rotation = (
                        self.rotation + 2
                    ) % 360  # Rotate 5 degrees to the right

    def apply_drag(self):
        # Apply drag - decrease current speed based on drag property
        if self.current_speed > 0:
            self.current_speed = max(0, self.current_speed - self.drag)
        elif self.current_speed < 0:
            self.current_speed = min(0, self.current_speed + self.drag)

    def speed_limiter(self, speed):
        return min(self.max_speed, max(-(self.max_speed / 2), speed))

    def move(self, timedelta, collisions):  # Override the default with player controls.
        # Calculate the new x and y position based on the rotation.
        # In this case, we're assuming that a rotation of 0 means the car is facing up
        # (negative y direction), and rotations are in degrees.
        # Store the current position
        if len(collisions) > 0:
            self.current_speed = 0
            return

        # Convert rotation to radians for math functions
        rad = math.radians(self.rotation)

        dx = self.current_speed * math.sin(rad) * timedelta
        dy = -self.current_speed * math.cos(rad) * timedelta

        # Update the position
        # TODO: Handle collision before we set the actual X and Y
        if self.x + dx <= 1920 - self.width and self.x + dx >= 0:
            self.x += dx

        if self.y + dy <= 1080 - self.height and self.y + dy >= 0:
            self.y += dy

        if len(collisions) > 0:
            for collision in collisions:
                print(
                    f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:Collision with {collision.component_name} detected ({collision.x},{collision.y}) ({collision.width * collision.get_scale()}, {collision.height * collision.get_scale()})"
                )

        self.prev_x = self.x
        self.prev_y = self.y
