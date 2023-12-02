import pygame

from Engine.component import Component
from Engine.text_component import TextComponent

BUTTON_CLICK = pygame.USEREVENT + 5

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
                 centered=True,
                 hover_color=(200, 200, 200)):
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
            (pos[0] + width/2, pos[1] + height/2),
            0,
            0,
            0,
            1.00
        )
        self.hover_color = hover_color
        self.hovered = False
        self.selected = False
    
    def update(self, delta_time, user_input):
        pass

    def handle_event(self, event):
        if self.get_button_collision() is True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_collision = pygame.event.Event(BUTTON_CLICK, button=self)
                pygame.event.post(button_collision)

            self.hovered = True
        elif self.selected is False:
            self.hovered = False
        
        return super().handle_event(event)

    def get_button_collision(self):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pygame.mouse.get_pos())

    def get_color(self):
        if self.hovered is True:
            return self.hover_color
        else:
            return pygame.Color(100, 100, 100)
    
    def reset(self):
        self.hovered = False
        self.selected = False
    
    def draw(self, screen, pos=None, scale=None):
        super().draw(screen, pos, scale=scale)

        if self.text_component is not None:
            self.text_component.draw(screen)

        if self.hovered is True:
            pygame.draw.rect(screen, self.get_color(), (self.x, self.y, self.width, self.height), 1)

