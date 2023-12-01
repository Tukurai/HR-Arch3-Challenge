import json
import time
from Settings import settings
from Server.base_client import BaseWebSocketClient
from server_game_data import ServerGameData


class WebSocketClient(BaseWebSocketClient):
    def __init__(self, uri, logging=False):
        super().__init__(uri, logging)
        self.game_data = ServerGameData()

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
    # Business Logic Methods
    ###########################

    def handle_active_players_msg(self, message):
        raise NotImplementedError("This method (handle_player) is not yet implemented")

    def handle_highscore_msg(self, message):
        raise NotImplementedError("This method (handle_highscore) is not yet implemented")


# Example usage
if __name__ == "__main__":
    client = WebSocketClient("wss://socketsbay.com/wss/v2/1/demo/")

    # Example sending a message
    client.send_message(json.dumps({"action": "request_latest_players", "params": {"name": "This player name"}}))

    # Simulate main program running
    try:
        while True:
            if(settings.DEBUG_MODE): print("Main loop doing stuff")
            # Example sending a message
            client.send_message(json.dumps({"action": "greet", "params": {"name": "Alice"}}))
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()
