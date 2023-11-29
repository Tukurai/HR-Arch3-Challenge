import pygame


class CollisionManager:
    def __init__(self, scene_manager, race_scene):
        self.scene_manager = scene_manager
        self.race_scene = race_scene

    def update(self, timedelta, input_state):
        # Calculate the move of objects that move, such as cars.
        # Calculate them against objects that are not itself.

        level = self.race_scene.level
        players = self.race_scene.players.values()

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
                player_i_scale = players[i].get_scale()
                mask1 = pygame.transform.scale(
                    players[i].mask_layers[0], (players[i].width * player_i_scale, players[i].height * player_i_scale)
                )
                player_j_scale = players[j].get_scale()
                mask2 = pygame.transform.scale(
                    players[j].mask_layers[0], (players[j].width * player_j_scale, players[j].height * player_j_scale)
                )

                offset_x = players[j].x - players[i].x
                offset_y = players[j].y - players[i].y

                if mask1.overlap(mask2, (offset_x, offset_y)):
                    # Collision detected, add to collisions dict
                    collisions[players[i]].append(players[j])
                    collisions[players[j]].append(players[i])

    def check_road_objects_collision(self, level, players, collisions):
        for player in players:
            for obj in level["Objects"] + level["Roads"]:
                # Scaling the mask layers for collision
                player_scale = player.get_scale()
                player_mask = pygame.transform.scale(
                    player.mask_layers[0], (player.width * player_scale, player.height * player_scale)
                )
                obj_scale = obj.get_scale()
                obj_mask = pygame.transform.scale(
                    obj.mask_layers[0], (obj.width * obj_scale, obj.height * obj_scale)
                )

                offset_x = obj.x - player.x
                offset_y = obj.y - player.y

                if player_mask.overlap(obj_mask, (offset_x, offset_y)):
                    # Collision detected, add to collisions dict
                    collisions[player].append(obj)


if __name__ == "__main__":
    print("Ran collision_manager.py directly. Start application from game.py.")
