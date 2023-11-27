import math
from Manager import sprite_manager
import pygame

pygame.init()
pygame.display.set_mode((1, 1))
def create_sprite_sheet(sprites, file_name, width=None, height=None):
    """
    This bad boi takes the spritesheet we loaded in, and makes a new spritesheet
    in the order of the IDs so we can load this new sheet into Tiled and build
    levels with synced ID codes.
    :param sprites:
    :param file_name:
    :param width:
    :param height:
    :return:
    """
    num_sprites = len(sprites)
    if not width and not height:
            sprite_width, sprite_height = sprites[0].get_size()
    else:
        sprite_width = width
        sprite_height = height
    cols = rows = math.ceil(math.sqrt(num_sprites))

    sprite_sheet_width = cols * sprite_width
    sprite_sheet_height = rows * sprite_height

    sprite_sheet = pygame.Surface((sprite_sheet_width, sprite_sheet_height), pygame.SRCALPHA)

    x_offset = y_offset = 0
    for i, sprite in enumerate(sprites):
        sprite_sheet.blit(sprite, (x_offset, y_offset))
        x_offset += sprite_width
        if (i + 1) % cols == 0:
            x_offset = 0
            y_offset += sprite_height

    pygame.image.save(sprite_sheet, file_name)

if __name__ == '__main__':

    manager = sprite_manager.SpriteManager()

    sprites = []
    sheet_names = ["Objects", "Roads"]

    for sheet_name in sheet_names:
        for _, road_object in manager.sprites_by_id[sheet_name].items():
            sprites.append(road_object.sprite)
        create_sprite_sheet(sprites, f'{sheet_name}_sprite_sheet.png', 128,128)
