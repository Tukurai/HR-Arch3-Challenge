import pygame

from Engine.text_component import TextComponent
from Settings import settings
from Settings.user_events import TEXT_BOX_INPUT

COLOR_ACTIVE = pygame.Color("gray96")
COLOR_INACTIVE = pygame.Color("gray77")


class TextBox:
    """
    A text box that can be used to input text.
    saved_text_display postion is absolute.
    """

    def __init__(
        self,
        component_name: str,
        pos: tuple[int, int],
        width: int,
        height: int,
        rotation=0,
        depth=0.50,
        scale=None,
        text=None,
        font_size=0,
        centered=True,
        box_color_active=COLOR_ACTIVE,
        box_color_inactive=COLOR_INACTIVE,
        saved_text_display=None,
    ):
        self.text_component = TextComponent(
            component_name + "_textbox_text",
            text,
            font_size,
            centered,
            None,
            (pos[0] + width / 2, pos[1] + height / 2),
            0,
            0,
            0,
            1.00,
        )

        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.default_text = text
        self.active = False

        self.box_color_active = box_color_active
        self.box_color_inactive = box_color_inactive
        self.color = box_color_inactive
        self.saved_text_display = saved_text_display

    def update(self, timedelta, input_state):
        if self.active is False:
            if self.text_component.text == "":
                self.text_component.text = self.default_text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                if self.text_component.text == self.default_text:
                    self.text_component.text = ""
            else:
                self.active = False

            if self.active is True:
                self.color = self.box_color_active
            else:
                self.color = self.box_color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.send_text()
                    if settings.DEBUG_MODE:
                        print(
                            f"{self.text_component.component_name}: {self.text_component.text}"
                        )
                    self.text_component.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text_component.text = self.text_component.text[:-1]
                else:
                    if len(self.text_component.text) < 10:
                        self.text_component.text += event.unicode

    def send_text(self):
        if self.saved_text_display is not None:
            self.saved_text_display.text += self.text_component.text

        textbox_text = pygame.event.Event(TEXT_BOX_INPUT, player_name=self.text_component.text)
        pygame.event.post(textbox_text)

    def draw(self, screen, pos=None, scale=None):
        pygame.draw.rect(screen, self.color, self.rect, 2)

        if self.text_component is not None:
            self.text_component.draw(screen)

        if self.saved_text_display is not None:
            self.saved_text_display.draw(screen)
