import csv
import os
import pygame
from typing import Union

from Manager.sprite_manager import SpriteManager
from Engine.full_sprite_object import FullSpriteObject


class LevelManager():
    def __init__(self, sprite_manager: SpriteManager):
        self.sprite_manager = sprite_manager
        self.current_path = os.path.dirname(os.path.dirname(__file__))
        self.level_path = os.path.join(self.current_path, "Level", "LevelFiles")
        self.levels = {}
        self.load_levels()

    def get_level(self, name: str) -> dict:
        """
        Retrieve a level by its name (file name without extension)
        :param name:
        :return: A dict with {Road: list[FullSpriteObject], Objects: list[FullSpriteObject]}
        """
        if name in self.levels.keys():
            return self.levels[name]
        else:
            print(f"Error -- LevelManager.get_level():  Level {name} not found!")

    def load_levels(self):
        """
        Finds all levels in the level folder and loads them into the LevelManager.levels
        :return:
        """
        files = self.find_files()
        print("-------  Loading levels ---------")
        for map_name in files:
            print(f"Loading [Level] : {map_name}")
            csv_map = self.convert_csv_to_id_array(map_name)
            self.levels[map_name] = {}
            # Attention, the resulting level layer is "Ground" but receives
            # its tiles from "Roads".
            self.levels[map_name]['Ground'] = self.convert_id_array_to_objects(csv_map['Ground'],
                                                                               "Roads")
            self.levels[map_name]['Roads'] = self.convert_id_array_to_objects(csv_map['Roads'],
                                                                              "Roads")
            self.levels[map_name]['Objects'] = self.convert_id_array_to_objects(csv_map['Objects'],
                                                                                "Objects")
        print("------ All levels loaded -----------")

    def find_files(self) -> list[str]:
        """
        Searches for files in the level folder and checks them for validity
        :return: Returns a list of valid file names for map layers
        """
        file_names = []
        layer_suffixes = ["_Ground.csv", "_Roads.csv", "_Objects.csv"]
        for file_name in os.listdir(self.level_path):
            for layer_name in layer_suffixes:
                if layer_name in file_name:
                    name = file_name.replace(layer_name, "")
                    if name not in file_names:
                        file_names.append(name)
        return file_names

    def convert_csv_to_id_array(self, map_name: str) -> dict:
        """
        Converts a Tiled-generated map csv into a dict with 2d-arrays for each layer
        :param map_name: Name of the map you want to convert
        :return: dict{layer1:[ids],layer2:[ids], etc}
        """
        layers = ["Ground", "Roads", "Objects"]
        layer_dict = {}
        for layer in layers:
            # Convert layers
            layer_path = os.path.join(self.level_path, f"{map_name}_{layer}.csv")
            print(f"Converting '{layer}' layer from: {layer_path}")
            with open(layer_path, newline='') as file:
                reader = csv.reader(file)
                array_2d = [list(map(int, row)) for row in reader]
                layer_dict[layer] = array_2d
        return layer_dict

    def convert_id_array_to_objects(self, id_array: list[list], category: str) -> list[
        list[Union[FullSpriteObject, None]]]:
        """
        Converts 2d-array with tile IDs into 2d-array of FullSpriteObjects
        :param id_array: The array you want to convert
        :param category: The category of spritesheet like "Roads" or "Objects"
        :return: A list of [FullSpriteObjects or None] (if empty tile)
        """
        object_array = []
        for index, id_row in enumerate(id_array):
            object_array.append([])
            for item in id_row:
                # Check for empty tiles
                if item == -1:
                    object_array[index].append(None)
                else:
                    object_array[index].append(
                        self.sprite_manager.get_sprite_object(category, item))

        return object_array


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode((1, 1))

    manager = LevelManager(SpriteManager())
    level = manager.get_level("testmap")
    print(level)
