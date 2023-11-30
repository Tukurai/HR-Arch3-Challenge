import pygame

from Engine.component import Component


class FullSpriteObject(Component):
    def __init__(self,
                 file_name: str,
                 tile_id: int,
                 sprite: pygame.Surface,
                 width: int,
                 height: int,
                 mask_layers: dict[int, pygame.Surface] = None,
                 scale=None):
        super().__init__(
            component_name=file_name,
            sprite=sprite,
            pos=(0,0),
            width=width,
            height=height,
            rotation=0,
            depth=0.50,
            scale=scale,
            mask_layers=mask_layers
        )
        self.tile_id = tile_id

    def __repr__(self):
        return (f" --- Filename: {self.component_name} --- "
                f"Amount of mask layers: {len(self.mask_layers)} --- "
                f"Width: {self.width} --- "
                f"Height: {self.height} --- "
                f"Tile ID: {self.tile_id} --- "
                f"Scale: {self.scale}")
