import pygame

from Settings import settings


class Component:
    def __init__(
        self,
        component_name,
        sprite,
        x,
        y,
        width,
        height,
        rotation,
        depth,
        color=None,
        scale=None,
        mask_layers: dict[int, pygame.Surface] = None,
    ):
        self.component_name = component_name
        self.sprite = sprite
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.depth = depth
        self.scale = scale
        self.mask_layers = mask_layers

        if color is not None and self.sprite is None:
            # Create a surface with dimensions 1792x896
            surface = pygame.Surface((width, height))

            # Fill the surface with the color (40, 40, 40)
            surface.fill(color)

            # Set the sprite
            self.sprite = surface

    def handle_event(self, event):
        pass

    def update(self, timedelta, input_state):
        pass

    def draw(self, screen, x=None, y=None, rotation=None, scale=None):
        drawx = self.x
        drawy = self.y

        if x is not None:
            drawx = x

        if y is not None:
            drawy = y

        object_scale = self.get_scale(scale)

        sprite_to_draw = self.sprite
        if 1.0 != object_scale:
            sprite_to_draw = pygame.transform.scale_by(sprite_to_draw, object_scale)

        if rotation is not None:
            # Create a new surface with the image, rotated
            sprite_to_draw = pygame.transform.rotate(sprite_to_draw, -self.rotation)

            # Calculate the new upper left corner position of the rotated car
            rect = sprite_to_draw.get_rect(
                center=self.sprite.get_rect(topleft=(self.x, self.y)).center
            )

            drawx = rect.topleft[0]
            drawy = rect.topleft[1]

        screen.blit(sprite_to_draw, (drawx, drawy))

    def get_scale(self, scale=None):
        object_scale = 1.0
        if self.scale is not None:
            object_scale = self.scale
        if scale is not None:
            object_scale = scale
        object_scale *= settings.GAME_SCALE
        return object_scale
