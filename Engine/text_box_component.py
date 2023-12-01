import pygame

from Engine.component import Component
from Engine.text_component import TextComponent

COLOR_ACTIVE = pygame.Color("gray96")
COLOR_INACTIVE = pygame.Color('gray77')

class TextBoxComponent(Component):
    def __init__(self,
                 file_name: str,
                 pos: tuple[int, int],
                 width: int,
                 height: int,
                 depth=0.50,
                 scale=None,
                 text=None,
                 font_size=0,
                 centered=False,
                 box_color_active=COLOR_ACTIVE,
                 box_color_inactive=COLOR_INACTIVE):
        super().__init__(
            component_name=file_name,
            sprite=None,
            pos=pos,
            width=width,
            height=height,
            rotation=0,
            depth=depth,
            scale=scale
        )
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text = TextComponent(
            file_name + "_textbox_text",
            text,
            font_size,
            centered,
            None,
            (pos[0], pos[1]),
            0,
            0,
            0,
            1.00
        )
        self.active = False
        self.box_color_active = box_color_active
        self.box_color_inactive = box_color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
                if self.active is True:
                    self.color = self.box_color_active
                else:  
                    self.color = self.box_color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(f"{self.text.component_name}: {self.text.text}")
                    self.text.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text.text = self.text[:-1]
                else:
                    self.text.text += event.unicode

    def get_button_collision(self):
        return pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pygame.mouse.get_pos())
    
    def draw(self, screen, pos=None, scale=None):
        super().draw(screen, pos, scale=scale)

        if self.text_component is not None:
            self.text_component.draw(screen)
    
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

