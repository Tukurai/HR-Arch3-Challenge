from Server.client import WebSocketClient
from Settings.user_events import DRIVE_CAR_EVENT, SUBMIT_SCORE_EVENT


class ServerManager:
    def __init__(self, ws_client: WebSocketClient):
        self.scores = {
            "map_left": None,
            "map_right": None,
            "map_up": None,
            "map_down": None,
            "map_complex": None,
        }

    def handle_event(self, event):
        if event.type == DRIVE_CAR_EVENT:
            pass
        if event.type == SUBMIT_SCORE_EVENT:
            pass

    def update(self, timedelta, input_state):
        pass

    def draw(self, screen):
        pass