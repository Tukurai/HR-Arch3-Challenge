import pygame

from Settings import settings


class CollisionManager:
    def __init__(self, scene_manager, race_scene):
        self.scene_manager = scene_manager
        self.race_scene = race_scene

    def update(self, timedelta, input_state):
        # Calculate the move of objects that move, such as cars.
        # Calculate them against objects that are not itself.

        level = self.race_scene.level
        players = self.race_scene.players

        # Initialize collisions dictionary
        collisions = {player: [] for player in players}

        # Check collision against other players
        self.check_players_collision(players, collisions)

        # Check collision against road and objects
        self.check_road_objects_collision(level, players, collisions)

        # After all collisions are checked, move the cars
        for player, collision_objs in collisions.items():
            player.move(timedelta, collision_objs)

    def check_players_collision(self, players, collisions):
        for i in range(len(players)):
            for j in range(i + 1, len(players)):
                # Scaling the mask layers for collision
                mask_i = pygame.mask.from_surface(
                    players[i].get_scaled_rotated_sprite_or_mask(
                        players[i].mask_layers[0]
                    )[0]
                )

                mask_j = pygame.mask.from_surface(
                    players[j].get_scaled_rotated_sprite_or_mask(
                        players[j].mask_layers[0]
                    )[0]
                )
                if mask_i.overlap(
                    mask_j, (players[j].x - players[i].x, players[j].y - players[i].y)
                ):
                    # Collision detected, add to collisions dict
                    collisions[players[i]].append(players[j])
                    collisions[players[j]].append(players[i])

    def check_road_objects_collision(self, level, players, collisions):
        for player in players:
            for obj in level["Objects"] + level["Roads"]:
                player_mask = pygame.mask.from_surface(
                    player.get_scaled_rotated_sprite_or_mask(
                        player.mask_layers[0]
                    )[0]
                )

                obj_mask = pygame.mask.from_surface(
                    obj.get_scaled_rotated_sprite_or_mask(
                        obj.mask_layers[0]
                    )[0]
                )

                if player_mask.overlap(obj_mask, (obj.x - player.x, obj.y - player.y)):
                    # Collision detected, add to collisions dict
                    collisions[player].append(obj)


if __name__ == "__main__":
    if(settings.DEBUG_MODE): print("Ran collision_manager.py directly. Start application from game.py.")
