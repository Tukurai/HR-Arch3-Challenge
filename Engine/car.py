import datetime
import math
import pygame
from Engine.component import Component
from Enums.direction import Direction
from Settings import settings

DRIVE_CAR_EVENT = pygame.USEREVENT + 1
RESET_CAR_EVENT = pygame.USEREVENT + 2


class Car(Component):
    def __init__(self, max_speed, drag, component_name, full_sprite, depth):
        super().__init__(
            component_name,
            full_sprite.sprite,
            (0, 0),
            full_sprite.width,
            full_sprite.height,
            depth,
            scale=settings.CAR_SCALE,
            mask_layers=full_sprite.mask_layers,
        )
        self.max_speed = max_speed
        self.drag = drag
        self.current_speed = 0
        self.prev_speed = 0
        self.prev_x = 0
        self.prev_y = 0

        self.current_checkpoint = 0
        self.next_checkpoint = 1
        self.lap = 0
        self.penalties = 0
        self.timeout = 0

    def handle_event(self, event):
        pass

    def update(self, timedelta, input_state):
        pass

    def draw(self, screen):
        super().draw(screen)

    def handle_controls(self, direction):
        match (direction):
            case Direction.UP:
                self.set_current_speed(self.speed_limiter(self.current_speed + 3))
            case Direction.DOWN:
                self.set_current_speed(self.speed_limiter(self.current_speed - 6))
            case Direction.LEFT:
                if self.current_speed != 0:
                    self.rotation_direction = Direction.LEFT
                    self.rotation = (self.rotation - 3) % 360
            case Direction.RIGHT:
                if self.current_speed != 0:
                    self.rotation_direction = Direction.RIGHT
                    self.rotation = (self.rotation + 3) % 360

    def apply_drag(self):
        # Apply drag - decrease current speed based on drag property
        if self.current_speed > 0:
            self.set_current_speed(max(0, self.current_speed - self.drag))
        elif self.current_speed < 0:
            self.set_current_speed(min(0, self.current_speed + self.drag))

    def speed_limiter(self, speed):
        return min(self.max_speed, max(-(self.max_speed / 2), speed))

    def set_current_speed(self, speed):
        self.prev_speed = self.current_speed
        self.current_speed = speed

    def move(self, timedelta, collisions):  # Override the default with player controls.
        # Calculate the new x and y position based on the rotation.
        # In this case, we're assuming that a rotation of 0 means the car is facing up
        # (negative y direction), and rotations are in degrees.

        drive_car = pygame.event.Event(DRIVE_CAR_EVENT, car=self)
        pygame.event.post(drive_car)

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
                if isinstance(collision, Car):
                    self.current_speed *= 0.2
                else:
                    self.timeout += 1
                    self.current_speed *= 0.9

                if settings.DEBUG_MODE:
                    print(
                        f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:Collision with {collision.component_name} detected ({collision.x},{collision.y}) ({collision.width * collision.get_scale()}, {collision.height * collision.get_scale()})"
                    )
        else:
            if self.timeout > 0:
                self.timeout -= 1

        if self.timeout > 30:
            self.reset_to_last_checkpoint()

        self.prev_x = self.x
        self.prev_y = self.y

    def reset_to_last_checkpoint(self):
        self.penalties += 1
        self.timeout = 0
        self.current_speed = 0

        reset_car = pygame.event.Event(RESET_CAR_EVENT, car=self)
        pygame.event.post(reset_car)
