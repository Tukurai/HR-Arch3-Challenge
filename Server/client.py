import json
import threading
import time
from Settings import settings
from Server.base_client import BaseWebSocketClient
from server_game_data import ServerGameData


class WebSocketClient(BaseWebSocketClient):
    def __init__(self, uri=None):
        super().__init__(uri)
        self.game_data = ServerGameData()
        self.message_router = {
            "active_players": self.handle_active_players_msg,
            "highscores": self.handle_highscore_msg,
        }
        self.lock = threading.Lock()

    ###########################
    # Thread-Safe Getters and Setters
    ###########################

    def update_highscores(self, highscores):
        with self.lock:
            self.game_data.highscores = highscores

    def update_active_players(self, active_players):
        with self.lock:
            self.game_data.active_players = active_players

    def get_highscores(self, level_name: str):
        with self.lock:
            return self.game_data.highscores[level_name]

    def get_active_players(self):
        with self.lock:
            return self.game_data.active_players

    ###########################
    # Handle Incoming Msg Methods
    ###########################

    def handle_active_players_msg(self, active_players: list[str]):
        print(f"Received -- Active players: {active_players}")
        self.update_active_players(active_players)

    def handle_highscore_msg(self, highscores: list[(int, str, str)]):
        print(f"Received -- Highscores: {highscores}")
        self.update_highscores(highscores)

    ###########################
    # Outgoing Msg Methods
    ###########################

    def send_active_player_msg(self, player_name: str):
        self.send_message(
        json.dumps({
            "action": "register_player",
            "params": {"name": f"{player_name}"}
        }))

    def send_highscore_msg(self, highscore: int, player_name: str, level_name: str):
        self.send_message(json.dumps({
            "action": "register_highscore",
            "params": {
                "name": f"{player_name}",
                "highscore": highscore,
                "level": f"{level_name}"
            }}))


# Example usage
if __name__ == "__main__":
    from random import randint, choice

    client = WebSocketClient("Salih_TEST")
    players = ["Marijn", "Jeroen", "Salih", "Niek", "Jesse", "Jasper"]
    levels = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]

    # Simulate main program running
    try:
        while client.running:
            if (settings.DEBUG_MODE): print("Main loop doing stuff")
            # Example sending a message
            client.send_active_player_msg(choice(players))
            time.sleep(1)
            client.send_message(json.dumps({
                "action": "register_highscore",
                "params": {
                    "name": f"{choice(players)}",
                    "highscore": randint(0, 10000),
                    "level": f"{choice(levels)}"
                }
            }))
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()
