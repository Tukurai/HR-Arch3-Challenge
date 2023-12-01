import pygame
from typing import Tuple
from Settings import settings


class Component:
    """Base class for all components that need to be rendered, and have need for update and event handling"""

    def __init__(
        self,
        component_name: str,
        sprite: pygame.Surface,
        pos: Tuple[int, int],
        width: float,
        height: float,
        rotation: float = 0,
        depth: float = 0.50,
        color: Tuple[int, int, int] = None,
        scale: float = None,
        mask_layers: dict[int, pygame.Surface] = None,
    ):
        self.component_name = component_name
        self.sprite = sprite
        self.x = pos[0]
        self.y = pos[1]
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
        """Handles the events passed down from the engine"""
        pass

    def update(self, timedelta, input_state):
        """Updates the component, generally overridden by the child class"""
        pass

    def draw(self, screen, pos=None, scale=None):
        """Draws the sprite to the screen, if x, y, rotation or scale are not None, it will override the objects values"""
        draw_pos = (self.x, self.y)

        if pos is not None:
            draw_pos = pos

        sprite = self.get_scaled_rotated_sprite_or_mask(self.sprite, scale)
        screen.blit(sprite[0], draw_pos + sprite[1])

        if self.mask_layers is not None:
            mask = self.get_scaled_rotated_sprite_or_mask(self.mask_layers[0], scale)
            screen.blit(mask[0], draw_pos + mask[1])

    def get_scale(self, scale: float = None) -> float:
        """Returns the scale of the object, this has an order of precedence: scale parameter, object scale, default scale"""
        object_scale = 1.0
        if self.scale is not None:
            object_scale = self.scale
        if scale is not None:
            object_scale = scale
        object_scale *= settings.GAME_SCALE
        return object_scale

    def get_scaled_rotated_sprite_or_mask(
        self, sprite_or_mask: pygame.Surface, scale: float = None
    ) -> Tuple[pygame.Surface, Tuple[int, int]]:
        """Returns a scaled and rotated sprite or mask surface, also return the center offset as a tuple (x, y)"""
        object_scale = self.get_scale(scale)
        sprite_to_draw = sprite_or_mask
        sprite_to_draw = pygame.transform.scale(
            sprite_to_draw,
            (
                int(self.width * object_scale),
                int(self.height * object_scale),
            ),
        )

        center_offset_x = 0
        center_offset_y = 0
        if self.rotation is not None:
            # Create a new surface with the image, rotated
            sprite_to_draw = pygame.transform.rotate(sprite_to_draw, -self.rotation)
            # Calculate the new upper left corner position of the rotated car
            rect = sprite_to_draw.get_rect()
            original_rect = self.sprite.get_rect(topleft=(self.x, self.y))

            center_offset_x = original_rect.centerx - rect.centerx
            center_offset_y = original_rect.centery - rect.centery

        return (sprite_to_draw, (center_offset_x, center_offset_y))
