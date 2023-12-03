import pygame

from Engine.component import Component
from Engine.text_component import TextComponent
from Settings.user_events import BUTTON_CLICK


class ButtonComponent(Component):
    def __init__(self,
                 file_name: str,
                 sprites: tuple[pygame.Surface, pygame.Surface, pygame.Surface],
                 pos: tuple[int, int],
                 depth=0.50,
                 scale=None,
                 text=None,
                 font_size=0,
                 centered=True,):
        super().__init__(
            component_name=file_name,
            sprite=sprites[0],
            pos=pos,
            width=sprites[0].sprite.get_width(),
            height=sprites[0].sprite.get_height(),
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
            (pos[0] + sprites[0].sprite.get_width()/2, pos[1] + sprites[0].sprite.get_height()/2),
            0,
            0,
            0,
            1.00
        )
        self.sprites = sprites
        self.hover = False
        self.active = False
    
    def update(self, delta_time, user_input):
        if self.get_button_collision() is True:
            self.hover = True
        else:
            self.hover = False
            self.active = False
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover is True:
                self.active = True
        if event.type == pygame.MOUSEBUTTONUP:
            if self.hover is True and self.active is True:
                self.active = False
                button_collision = pygame.event.Event(BUTTON_CLICK, button=self)
                pygame.event.post(button_collision)
            self.hover = False
        
        return super().handle_event(event)

    def get_button_collision(self):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pygame.mouse.get_pos())
    
    def draw(self, screen, pos=None, scale=None):
        if self.active:
            self.sprite = self.sprites[2].sprite
        elif self.hover:
            self.sprite = self.sprites[1].sprite
        else:
            self.sprite = self.sprites[0].sprite

        super().draw(screen, pos, scale=scale)

        if self.text_component is not None:
            self.text_component.draw(screen)

