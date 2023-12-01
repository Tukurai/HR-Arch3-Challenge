import asyncio
import json
import time

import websockets
import threading


class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self.start_loop, args=(self.loop,))
        self.thread.start()

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.connect())

    async def connect(self):
        async with websockets.connect(self.uri) as websocket:
            await self.listen(websocket)

    async def listen(self, websocket):
        async for message in websocket:
            print(f"Received message: {message}")

    def send_message(self, message):
        asyncio.run_coroutine_threadsafe(self._send(message), self.loop)

    async def _send(self, message):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(message)

    def close(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()


# Example usage
if __name__ == "__main__":
    client = WebSocketClient("wss://socketsbay.com/wss/v2/1/demo/")

    # Example sending a message
    client.send_message(json.dumps({"action": "greet", "params": {"name": "Alice"}}))

    # Simulate main program running
    try:
        while True:
            print("Main loop doing stuff")
            # Example sending a message
            client.send_message(json.dumps({"action": "greet", "params": {"name": "Alice"}}))
            time.sleep(1)
    except KeyboardInterrupt:
        client.close()