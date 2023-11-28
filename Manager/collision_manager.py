import pygame


class CollisionManager:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

    def update(self, timedelta, input_state):
        # Calculate the move of objects that move, such as cars. 
        # Calculate them against objects that are not itself.
        
        self.active_scene.update(timedelta, input_state)


if __name__ == "__main__":
    print("Ran collision_manager.py directly. Start application from game.py.")
