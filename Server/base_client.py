import asyncio
import json
import time
import websockets
import threading
from Settings import settings
from abc import ABC


class BaseWebSocketClient(ABC):
    def __init__(self, uri: str = None, port: str = None):
        # Server Settings from settings file
        self.uri = uri if uri else settings.SERVER_URI
        self.port = port if port else settings.SERVER_PORT
        self.logging = settings.SERVER_DEBUG_MODE

        # Asyncio and Threading startup
        self.websocket = None
        self.running = True
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
        if self.uri:
            try:
                if self.logging:
                    print(f"Connecting to {self.uri}:{self.port}")
                self.websocket = await websockets.connect(f"{self.uri}:{self.port}")
                await self.listen(self.websocket)
            except ConnectionRefusedError:
                print(f"Could not connect to {self.uri}:{self.port}\n"
                      "Reason: Connection refused")
                self.close()

    async def listen(self, websocket):
        async for message in websocket:
            await self.handle_message(message)

    def send_message(self, message):
        if self.logging:
            print(f"Sending message: {message}")
        if not self.websocket:
            time.sleep(1)
        if self.websocket and self.websocket.closed:
            self.loop.run_until_complete(self.connect())
        if self.websocket and not self.websocket.closed:
            asyncio.run_coroutine_threadsafe(self._send(message), self.loop)
        else:
            print("WebSocket is closed. Cannot send message.")

    async def _send(self, message):
        try:
            await self.websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection is closed.")

    def close(self):
        self.running = False
        if self.websocket:
            asyncio.run_coroutine_threadsafe(self.websocket.close(), self.loop)
        self.loop.call_soon_threadsafe(self.loop.stop)
        print("Client closed.")

    ###########################
    # Message Handling Methods
    ###########################

    # Function to handle incoming messages
    async def handle_message(self, message):
        data = json.loads(message)
        if self.logging:
            print(f"Received message: {message}")
        action = data.get("action")
        params = data.get("params", {})

        if action in self.message_router:
            response = self.message_router[action](**params)
            return response
        else:
            return "Unknown action"
