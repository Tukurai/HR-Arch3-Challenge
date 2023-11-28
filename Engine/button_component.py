import pygame

from Engine.component import Component
from Engine.text_component import TextComponent

class ButtonComponent(Component):
    def __init__(self,
                 file_name: str,
                 sprite: pygame.Surface,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 depth=0.50,
                 scale=None,
                 text=None,
                 font_size=0,
                 centered=True):
        super().__init__(
            component_name=file_name,
            sprite=sprite,
            x=x,
            y=y,
            width=width,
            height=height,
            rotation=0,
            depth=depth,
            scale=scale
        )
        self.text_component = TextComponent(
            file_name + "_text",
            text,
            font_size,
            centered,
            None,
            x + (width / 2),
            y - (height / 2),
            0,
            0,
            0,
            1.00
        )
    
    def draw(self, screen, x=None, y=None, rotation=None, scale=None):
        # This does not work yet...
        super().draw(screen, x=self.x, y=self.y, rotation=self.rotation, scale=self.scale)

        if self.text_component is not None:
            self.text_component.draw(screen)

