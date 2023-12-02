from Server import server_storage
from Server.base_client import BaseWebSocketClient
from Server.data_categories import GameDataType
from server_game_data import ServerGameData


class WebSocketServer(BaseWebSocketClient):
    def __init__(self, uri, logging=False):
        super().__init__(uri, logging)
        self.game_data = ServerGameData()
        self.game_data.highscores =  server_storage.retrieve_data(GameDataType.HIGH_SCORES)
        self.game_data.latest_players = server_storage.retrieve_data(
            GameDataType.LATEST_ACTIVE_PLAYERS)


    ###########################
    # Setup Methods
    ###########################

    def setup_message_router(self) -> dict[str, callable]:
        """
        Sets up the message router by adding actions and their corresponding methods.
        :return:
        """
        return {
            "subscribe": self.handle_subscribe,
            "unsubscribe": self.handle_unsubscribe,
            "echo": self.handle_echo,
            "register_player": self.handle_register_player,
        }

    def handle_subscribe(self, message):
        raise NotImplementedError("This method (handle_subscribe) is not yet implemented")

    def handle_unsubscribe(self, message):
        raise NotImplementedError("This method (handle_unsubscribe) is not yet implemented")

    def handle_echo(self, message):
        raise NotImplementedError("This method (handle_echo) is not yet implemented")

    def handle_register_player(self, message):
        raise NotImplementedError("This method (handle_register_player) is not yet implemented")