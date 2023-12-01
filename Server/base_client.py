import asyncio
import json
import time
import websockets
import threading
from abc import ABC, abstractmethod


class BaseWebSocketClient(ABC):
    def __init__(self, uri, logging=False):
        self.uri = uri
        self.logging = logging
        # Message Router
        self.message_router = self.setup_message_router()
        if not self.message_router:
            raise Exception("Message router not set up. Please add actions and their "
                            "corresponding methods.")
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

    ###########################
    # Setup Methods
    ###########################

    @abstractmethod
    def setup_message_router(self) -> dict[str, callable]:
        """
        Sets up the message router by adding actions and their corresponding methods.
        :return:
        """
        pass

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
            await self.handle_message(message)

    def send_message(self, message):
        asyncio.run_coroutine_threadsafe(self._send(message), self.loop)

    async def _send(self, message):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(message)

    def close(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

    ###########################
    # Message Handling Methods
    ###########################

    # Function to handle incoming messages
    async def handle_message(self, message):
        data = json.loads(message)
        action = data.get("action")
        params = data.get("params", {})
        if self.logging:
            print(f"Received message: {message}")

        if action in self.message_router:
            response = self.message_router[action](**params)
            return response
        else:
            return "Unknown action"