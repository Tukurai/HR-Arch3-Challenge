import pygame

from Engine.component import Component
from Engine.text_component import TextComponent

# TODO: Center the text when the button is scaled up...

class ButtonComponent(Component):
    def __init__(self,
                 file_name: str,
                 sprite: pygame.Surface,
                 pos: tuple[int, int],
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
            pos=pos,
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
            pos + ((width / 2), (height / 2) + 48),
            0,
            0,
            0,
            1.00
        )
    
    def draw(self, screen, pos=None, scale=None):
        super().draw(screen, pos, scale=scale)

        if self.text_component is not None:
            self.text_component.draw(screen)

