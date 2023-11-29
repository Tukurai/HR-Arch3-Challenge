import os
import pygame
from typing import Union
from Engine.spritesheet import Spritesheet
from Engine.full_sprite_object import FullSpriteObject
from Settings.relative_scale import SCALES


class SpriteManager:

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
        self.blue_ui = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "blueSheet.png")
        )
        self.green_ui = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "greenSheet.png")
        )
        self.red_ui = Spritesheet(
            os.path.join(current_path, "Assets", "Sprites", "redSheet.png")
        )

        self.sprites_by_name = {}
        self.sprites_by_id = {}
        self.populate_library_items("Cars", self.cars_spritesheet)
        self.populate_library_items("Objects", self.objects_spritesheet)
        self.populate_library_items("Roads", self.roads_spritesheet)
        self.populate_library_items("UI", self.blue_ui)
        self.populate_library_items("UI", self.green_ui)
        self.populate_library_items("UI", self.red_ui)

    def populate_library_items(self, category: str, sprite_sheet: Spritesheet):
        atlas = sprite_sheet.sprite_atlas
        index_offset = 0
        if category not in self.sprites_by_name:
            # This library doesn't exist yet, so we populate a key for the category
            self.sprites_by_name[category] = {}
            self.sprites_by_id[category] = {}
        else:
            # This library is already populated, so we offset its index
            index_offset = list(self.sprites_by_name[category].values())[-1].tile_id + 1
        for index, file_name in enumerate(atlas.keys()):
            width = atlas[file_name]['w']
            height = atlas[file_name]['h']
            sprite = sprite_sheet.get_sprite(file_name)
            masks = sprite_sheet.get_mask_from_all_layers(file_name)
            scale = SCALES.get(file_name)

            # Create the object
            sprite_object = FullSpriteObject(file_name,
                                             index + index_offset,
                                             sprite, width, height,
                                             mask_layers=masks,
                                             scale=scale)

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
        Get a FullSpriteObject of a car by its ID or filename

        :param sprite_id: The name (str) or id (int) of the tile
        :return: FullSpriteObject
        """
        return self.get_sprite_object("Cars", sprite_id)

    def get_object(self, sprite_id: Union[int, str]):
        """
        Get a FullSpriteObject of an object tile by its ID or filename

        :param sprite_id: The name (str) or id (int) of the tile
        :return: FullSpriteObject
        """
        return self.get_sprite_object("Objects", sprite_id)

    def get_ui_element(self, sprite_id: Union[int, str]):
        """
        Get a FullSpriteObject of an UI element by its ID or filename

        :param sprite_id: The name (str) or id (int) of the tile
        :return: FullSpriteObject
        """
        return self.get_sprite_object("UI", sprite_id)

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
