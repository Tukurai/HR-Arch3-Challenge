from Engine.component import Component
import pygame


class TextComponent(Component):
    def __init__(
        self, component_name, text, sprite, x, y, width, height, rotation, depth
    ):
        super().__init__(component_name, sprite, x, y, width, height, rotation, depth)
        self.text = text

    def handle_events(self):
        print(f"DEBUG: {self.component_name} triggered 'handle_events()'.")

    def update(self, timedelta, input_state):
        print(
            f"DEBUG: {self.component_name} triggered 'update({timedelta}, {input_state})'."
        )

    def draw(self, screen):
        # Set up the font
        font = pygame.font.Font(None, 36)

        # Render the text
        rendered_text = font.render(self.text, True, (255, 255, 255))

        # Draw the text
        screen.blit(rendered_text, self.x, self.y)
