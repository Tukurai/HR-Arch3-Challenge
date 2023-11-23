from Engine.component import Component
import pygame


class TextComponent(Component):
    def __init__(
        self,
        component_name,
        text,
        font_size,
        centered,
        sprite,
        x,
        y,
        width,
        height,
        rotation,
        depth,
    ):
        super().__init__(component_name, sprite, x, y, width, height, rotation, depth)
        self.text = text
        self.font_size = font_size
        self.centered = centered

    def handle_event(self, event):
        pass

    def update(self, timedelta, input_state):
        pass

    def draw(self, screen):
        # Set up the font
        font = pygame.font.Font(None, self.font_size)

        # Render the text, and center it
        rendered_text = font.render(self.text, True, (255, 255, 255))
        drawX = self.x
        drawY = self.y

        if self.centered:
            rendered_text_size = font.size(self.text)
            drawX -= (rendered_text_size[0] / 2.0)
            drawY -= (rendered_text_size[1] / 2.0)

        # Draw the text
        screen.blit(rendered_text, (drawX, drawY))
