import pygame


class Component:
    def __init__(self, component_name, sprite, x, y, width, height, rotation, depth, color = None):
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

    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
