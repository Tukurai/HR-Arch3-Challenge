class ServerGameData:

    def __init__(self):
        self.active_players: list[str] = []
        self.highscores: dict[str, list] = {"map_left": [],
                                 "map_right": [],
                                 "map_up": [],
                                 "map_down": [],
                                 "map_complex": []}
        self.max_amount_of_players = 5
        self.max_amount_of_highscores = 10

    def ingest_player(self, player: str):
        if player in self.active_players:
            return
        if len(self.active_players) < self.max_amount_of_players:
            self.active_players.append(player)
        else:
            self.active_players.pop(0)
            self.active_players.append(player)

    def ingest_highscore(self, highscore: int, player:str, level_name:str):
        if level_name not in self.highscores:
            self.highscores[level_name] = []
        if len(self.highscores[level_name]) < self.max_amount_of_highscores:
            self.highscores[level_name].append((highscore, player))
        else:
            self.highscores[level_name] = sorted(self.highscores[level_name], key=lambda x: x[0])
            if highscore > self.highscores[level_name][0][0]:
                self.highscores[level_name][0] = (highscore, player)
                self.highscores[level_name] = sorted(self.highscores[level_name], key=lambda x: x[0])

    def __repr__(self):
        return (f"ServerGameData(latest_players={self.active_players} ---"
                f" highscores={self.highscores})")