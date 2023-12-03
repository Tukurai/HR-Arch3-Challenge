from Server.client import WebSocketClient
from Settings.user_events import SUBMIT_SCORE_EVENT, TEXT_BOX_INPUT


class ServerManager:
    def __init__(self):
        self.ws_client = WebSocketClient()
        self.scores = self.ws_client.game_data.highscores
        self.active_players = self.ws_client.game_data.active_players

    def handle_event(self, event):
        if event.type == SUBMIT_SCORE_EVENT:
            print(f"Sending high_score msg for: {event.name} -- {event.score}")
            self.ws_client.send_highscore_msg(event.score, event.name, event.level_name)
        if event.type == TEXT_BOX_INPUT:
            print(f"Sending active player msg: {event.player_name}")
            self.ws_client.send_active_player_msg(event.player_name)

    def update(self, timedelta, input_state):
        pass

    def draw(self, screen):
        pass
