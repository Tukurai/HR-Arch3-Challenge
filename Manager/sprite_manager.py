import os
import pygame
from types import SimpleNamespace

from Engine.spritesheet import Spritesheet


class FullSpriteObject:
    def __init__(
        self,
        sprite: pygame.Surface,
        width: int,
        height: int,
        masks_layers: dict[int, pygame.Surface] = None,
    ):
        self.sprite = sprite
        self.mask_layers = masks_layers
        self.width = width
        self.height = height


class SpriteManager:
    def __init__(self):
        current_path = os.path.dirname(os.path.dirname(__file__))

        self.cars_spritesheet = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "spritesheet_vehicles.png")
        )
        self.objects_spritesheet = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "spritesheet_objects.png")
        )
        self.roads_spritesheet = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "spritesheet_tiles.png"),
            mask_layer_amount=1,
        )
        
        self.game_object_library = {}
        self.populate_library_items("Cars", self.cars_spritesheet)
        self.populate_library_items("Objects", self.objects_spritesheet)
        self.populate_library_items("Roads", self.roads_spritesheet)

    def populate_library_items(self, category: str, sprite_sheet: Spritesheet):
        atlas = sprite_sheet.sprite_atlas
        self.game_object_library[category] = {}
        for key in atlas.keys():
            width = atlas[key]["w"]
            height = atlas[key]["h"]
            sprite = sprite_sheet.get_sprite(key)
            # TODO Add mask layers to FullSpriteObject
            self.game_object_library[category][key] = FullSpriteObject(
                sprite, width, height
            )


if __name__ == "__main__":
    pygame.init()
    DISPLAY_W, DISPLAY_H = 800, 300
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
    pygame.display.set_caption("Sprite Manager Tests")
    running = True

    # Here is where the magic happens
    manager = SpriteManager()
    library = manager.game_object_library

    print(library)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Make white background
        canvas.fill((0, 0, 0))
        # Place road sprite
        canvas.blit(library["Cars"]["car_black_1.png"].sprite, (50, DISPLAY_H - 200))
        # Place road sprite
        canvas.blit(
            library["Roads"]["road_asphalt01.png"].sprite, (200, DISPLAY_H - 200)
        )

        window.blit(canvas, (0, 0))
        pygame.display.update()
