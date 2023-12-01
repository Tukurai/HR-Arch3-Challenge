import asyncio
import json
import time
from Settings import settings
import websockets
import threading


class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        # Message Router
        self.message_router = {
            "players": self.handle_player_msg,
            "highscores": self.handle_highscore_msg
        }
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

    ###########################
    # Client Connection Methods
    ###########################

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect())

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            await self.listen(websocket)

    async def listen(self, websocket):
        async for message in websocket:
            if(settings.DEBUG_MODE): print(f"Received message: {message}")

    def send_message(self, message):
        asyncio.run_coroutine_threadsafe(self._send(message), self.loop)

    async def _send(self, message):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(message)

    def close(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

    ###########################
    # Business Logic Methods
    ###########################

    def handle_player_msg(self, message):
        raise NotImplementedError("This method (handle_player) is not yet implemented")

    def handle_highscore_msg(self, message):
        raise NotImplementedError("This method (handle_highscore) is not yet implemented")


    ###########################
    # Message Handling Methods
    ###########################

    # Function to handle incoming messages
    async def handle_message(self, message):
        data = json.loads(message)
        action = data.get("action")
        params = data.get("params", {})

        if action in self.message_router:
            response = self.message_router[action](**params)
            return response
        else:
            return "Unknown action"


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
