class ServerGameData:
    def __init__(self):
        self.players: list[str] = []
        self.highscores: list[int] = []
        self.max_amount_of_players = 5
        self.max_amount_of_highscores = 10

    def add_player(self, player: str):
        if len(self.players) < self.max_amount_of_players:
            self.players.append(player)
        else:
            self.players.pop(0)
            self.players.append(player)

    def add_highscore(self, highscore: int):
        if len(self.highscores) < self.max_amount_of_highscores:
            self.highscores.append(highscore)
        else:
            self.highscores.sort()
            if highscore > self.highscores[0]:
                self.highscores[0] = highscore
                self.highscores.sort()