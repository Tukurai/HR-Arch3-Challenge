import asyncio
import websockets

class GameServer:

    def __init__(self):
        self.queue = asyncio.Queue()

    async def send_data(self, websocket, path):
        while True:
            # Wait for a request or a signal to send data
            request = await websocket.recv()
            if request == "send data":
                data = "your data here"  # Fetch or generate the data
                await websocket.send(data)

    def start_server(self):
        start_server = websockets.serve(self.send_data, "localhost", 8765)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    # Create a GameServer instance and start the server
    game_server = GameServer()
    game_server.start_server()
    print("I swear I'm not blocking the main thread.")