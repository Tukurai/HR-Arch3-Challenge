import asyncio
import websockets


class GameServerClient:

    # WebSocket client function with queue as an argument
    async def client(self, queue):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            while True:
                data = await websocket.recv()
                queue.put(data)  # Put data into the queue

    # Function to run the client in a separate thread
    def start_client(self, queue):
        asyncio.new_event_loop().run_until_complete(self.client(queue))


