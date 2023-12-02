import asyncio

from Server import server_storage
from Server.base_client import BaseWebSocketClient
from Server.data_categories import GameDataType
from Settings import settings
from server_game_data import ServerGameData


class WebSocketServer(BaseWebSocketClient):
    def __init__(self, uri, logging=False):
        super().__init__(uri, logging)
        self.game_data = ServerGameData()
        self.game_data.highscores = server_storage.retrieve_data(GameDataType.HIGH_SCORES)
        self.game_data.latest_players = server_storage.retrieve_data(
            GameDataType.LATEST_ACTIVE_PLAYERS)
        self.active_connections: list = []

    ###########################
    # Setup Methods
    ###########################

    def setup_message_router(self) -> dict[str, callable]:
        """
        Sets up the message router by adding actions and their corresponding methods.
        :return:
        """
        return {
            "echo": self.handle_echo,
            "register_player": self.handle_register_player,
            "register_highscore": self.handle_register_highscore,
        }

    def handle_echo(self, message):
        raise NotImplementedError("This method (handle_echo) is not yet implemented")

    def handle_register_player(self, message):
        raise NotImplementedError("This method (handle_register_player) is not yet implemented")

    def handle_register_highscore(self, message):
        raise NotImplementedError("This method (handle_register_highscore) is not yet implemented")

    ###########################
    # Server Specific Methods
    ###########################

    def broadcast(self, message):
        # Broadcast a message to all active connections
        coros = [conn.send(message) for conn in self.active_connections if conn.open]
        if coros:
            asyncio.run_coroutine_threadsafe(asyncio.wait(coros), self.loop)
        elif settings.DEBUG_MODE:
            print(f"No active connections to broadcast message: {message}")

    async def listen(self, websocket):
        # Add the new websocket to the list of active connections
        self.active_connections.append(websocket)
        try:
            async for message in websocket:
                await self.handle_message(message)
        finally:
            # Remove the websocket from the list when it disconnects
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)