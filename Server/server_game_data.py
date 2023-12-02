class ServerGameData:

    def __init__(self):
        self.latest_players: list[str] = []
        self.highscores: list[(str, int)] = []
        self.max_amount_of_players = 5
        self.max_amount_of_highscores = 10

    def ingest_player(self, player: str):
        if player in self.latest_players:
            return
        if len(self.latest_players) < self.max_amount_of_players:
            self.latest_players.append(player)
        else:
            self.latest_players.pop(0)
            self.latest_players.append(player)

    def ingest_highscore(self, player:str, highscore: int):
        if len(self.highscores) < self.max_amount_of_highscores:
            self.highscores.append(highscore)
        else:
            self.highscores.sort()
            if highscore > self.highscores[0]:
                self.highscores[0] = highscore
                self.highscores.sort()
