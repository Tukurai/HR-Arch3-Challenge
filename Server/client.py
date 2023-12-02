import json
import time
from Settings import settings
from Server.base_client import BaseWebSocketClient
from server_game_data import ServerGameData


class WebSocketClient(BaseWebSocketClient):
    def __init__(self, player_name: str, uri=None):
        super().__init__(uri)
        self.game_data = ServerGameData()
        self.player_name = player_name

    ###########################
    # Setup Methods
    ###########################

    def setup_message_router(self) -> dict[str, callable]:
        """
        Sets up the message router by adding actions and their corresponding methods.
        :return:
        """
        pass

    ###########################
    # Handle Incoming Msg Methods
    ###########################

    def handle_active_players_msg(self, message):
        raise NotImplementedError("This method (handle_player) is not yet implemented")

    def handle_highscore_msg(self, message):
        raise NotImplementedError("This method (handle_highscore) is not yet implemented")

    ###########################
    # Outgoing Msg Methods
    ###########################

    def send_initial_msg(self):
        self.send_message(json.dumps({"action": "register_player", "params": {"name": self.player_name}}))

    def send_highscore_msg(self, highscore: int):
        self.send_message(json.dumps({"action": "register_highscore", "params": {
            "name": self.player_name,
            "highscore": highscore}}))

# Example usage
if __name__ == "__main__":
    client = WebSocketClient("Salih_TEST")

    # Simulate main program running
    try:
        while True:
            if (settings.DEBUG_MODE): print("Main loop doing stuff")
            # Example sending a message
            client.send_message(json.dumps({"action": "greet", "params": {"name": "Alice"}}))
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()
