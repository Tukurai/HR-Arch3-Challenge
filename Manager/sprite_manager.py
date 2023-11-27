import os
from typing import Union
from Engine.component import Component
import pygame
from Engine.spritesheet import Spritesheet


class FullSpriteObject(Component):
    def __init__(self,
                 file_name: str,
                 tile_id: int,
                 sprite: pygame.Surface,
                 width: int,
                 height: int,
                 masks_layers: dict[int, pygame.Surface] = None):
        super().__init__(
            component_name=file_name,
            sprite=sprite,
            x=0,
            y=0,
            width=width,
            height=height,
            rotation=0,
            depth=0.50,
        )
        self.mask_layers = masks_layers
        self.tile_id = tile_id

    def __repr__(self):
        return (f" --- Filename: {self.component_name} --- "
                f"Amount of mask layers: {len(self.mask_layers)} --- "
                f"Width: {self.width} --- "
                f"Height: {self.height} --- "
                f"Tile ID: {self.tile_id} --- ")


class SpriteManager():

    def __init__(self):
        current_path = os.path.dirname(os.path.dirname(__file__))

        self.cars_spritesheet = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "spritesheet_vehicles.png"),
            mask_layer_amount=1
        )
        self.objects_spritesheet = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "spritesheet_objects.png")
        )
        self.roads_spritesheet = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "spritesheet_tiles.png"),
            mask_layer_amount=1,
        )

        self.sprites_by_name = {}
        self.sprites_by_id = {}
        self.populate_library_items("Cars", self.cars_spritesheet)
        self.populate_library_items("Objects", self.objects_spritesheet)
        self.populate_library_items("Roads", self.roads_spritesheet)

    def populate_library_items(self, category: str, sprite_sheet: Spritesheet):
        atlas = sprite_sheet.sprite_atlas
        self.sprites_by_name[category] = {}
        self.sprites_by_id[category] = {}
        for index, file_name in enumerate(atlas.keys()):
            width = atlas[file_name]['w']
            height = atlas[file_name]['h']
            sprite = sprite_sheet.get_sprite(file_name)
            masks = sprite_sheet.get_mask_from_all_layers(file_name)
            # Create the object
            sprite_object = FullSpriteObject(file_name,
                                             index,
                                             sprite, width, height,
                                             masks_layers=masks)

            # Store it in two libraries, so we can look up by name and ID
            self.sprites_by_name[category][file_name] = sprite_object
            self.sprites_by_id[category][index] = sprite_object

            print(f"Loaded [FullSpriteObject]: {self.sprites_by_name[category][file_name]}")

    def get_road(self, sprite_id: Union[int, str]):
        """
        Get a FullSpriteObject of a road tile by its ID or filename

        :param sprite_id: The name (str) or id (int) of the tile
        :return: FullSpriteObject
        """
        return self.get_sprite_object("Roads", sprite_id)

    def get_car(self, sprite_id: Union[int, str]):
        """
        Get a FullSpriteObject of a road tile by its ID or filename

        :param sprite_id: The name (str) or id (int) of the tile
        :return: FullSpriteObject
        """
        return self.get_sprite_object("Cars", sprite_id)

    def get_object(self, sprite_id: Union[int, str]):
        """
        Get a FullSpriteObject of a road tile by its ID or filename

        :param sprite_id: The name (str) or id (int) of the tile
        :return: FullSpriteObject
        """
        return self.get_sprite_object("Objects", sprite_id)

    def get_sprite_object(self, category: str, sprite_id):
        if isinstance(sprite_id, str):
            if sprite_id in self.sprites_by_name[category]:
                return self.sprites_by_name[category][sprite_id]
            else:
                print(f"Error, '{sprite_id}' not found in Sprite Library ({category}) (by name).")
        if isinstance(sprite_id, int):
            if sprite_id in self.sprites_by_id[category]:
                return self.sprites_by_id[category][sprite_id]
            else:
                print(f"Error, '{sprite_id}' not found in Sprite Library ({category}) (by ID/Int).")


if __name__ == '__main__':
    pygame.init()
    DISPLAY_W, DISPLAY_H = 800, 300
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    window = pygame.display.set_mode(((DISPLAY_W, DISPLAY_H)))
    pygame.display.set_caption("Sprite Manager Tests")
    running = True

    # Here is where the magic happens
    manager = SpriteManager()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Make white background
        canvas.fill((0, 0, 0))
        # Place road sprite
        canvas.blit(manager.get_car(10).sprite,
                    (20, DISPLAY_H - 200))

        # Place road sprite
        canvas.blit(manager.get_road(47).sprite,
                    (140, DISPLAY_H - 200))
        # Place road mask
        canvas.blit(manager.get_road(47).mask_layers[0],
                    (300, DISPLAY_H - 200))

        window.blit(canvas, (0, 0))
        pygame.display.update()
