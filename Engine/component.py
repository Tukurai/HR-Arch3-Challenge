import pygame

from Settings import settings


class Component:
    def __init__(
        self, component_name, sprite, x, y, width, height, rotation, depth, color=None
    ):
        self.component_name = component_name
        self.sprite = sprite
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation
        self.depth = depth
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

    def draw(self, screen, x=None, y=None, rotation=None):
        drawx = self.x
        drawy = self.y

        if x is not None:
            drawx = x

        if y is not None:
            drawy = y

        sprite_to_draw = self.sprite
        if 1.0 != settings.GAME_SCALE:
            sprite_to_draw = pygame.transform.scale_by(
                sprite_to_draw, settings.GAME_SCALE
            )
        
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
