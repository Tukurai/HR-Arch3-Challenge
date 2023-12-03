from Server.client import WebSocketClient
from Settings.user_events import SUBMIT_SCORE_EVENT, START_RACE_EVENT


class ServerManager:
    def __init__(self):
        self.ws_client = WebSocketClient()
        self.scores = self.ws_client.game_data.highscores
        self.active_players = self.ws_client.game_data.active_players

    def handle_event(self, event):
        if event.type == SUBMIT_SCORE_EVENT:
            self.ws_client.send_highscore_msg(event.score, event.player_name, event.level_name)
        if event.type == START_RACE_EVENT:
            self.ws_client.send_active_player_msg(event.player_name)

    def update(self, timedelta, input_state):
        pass

    def draw(self, screen):
        pass
