import asyncio
import websockets
import json
import threading
from server_game_data import ServerGameData
from Settings import settings


class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected = set()
        self.server = None
        self.loop = asyncio.new_event_loop()
        self.game_data = ServerGameData()
        self.debug = settings.SERVER_DEBUG_MODE

    async def broadcast_data(self, msg):
        if self.connected:
            if self.debug:
                print(f"Broadcasting data: {str(self.game_data)} to {len(self.connected)} clients")
            await asyncio.wait([asyncio.create_task(
                user.send(json.dumps(msg))) for user in self.connected])

    async def handler(self, websocket, path):
        self.connected.add(websocket)
        try:
            async for message in websocket:
                if self.debug:
                    print(f"Received message: {message}")
                data = json.loads(message)
                if "action" in data:
                    match data["action"]:
                        case "register_highscore":
                            self.game_data.ingest_highscore(data["params"]["highscore"],
                                                            data["params"]["name"],
                                                            data["params"]["level"])
                            msg = {"action": "highscores",
                                   "params": {"highscores": self.game_data.highscores}}
                            await self.broadcast_data(msg)
                        case "register_player":
                            self.game_data.ingest_player(data["params"]['name'])
                            msg = {"action": "active_players",
                                   "params": {"active_players": self.game_data.active_players}}
                            await self.broadcast_data(msg)
                        case _:
                            print(f"Unknown action: {data['action']}")
                    print(self.game_data)
                else:
                    print(f"Unknown message type: {message}")
        finally:
            self.connected.remove(websocket)

    def start_server(self):
        if self.debug:
            print(f"Setting up event loop for {threading.current_thread().name}")
        asyncio.set_event_loop(self.loop)  # Set the event loop for this thread
        server_coroutine = websockets.serve(self.handler, self.host, self.port)
        self.server = asyncio.ensure_future(server_coroutine, loop=self.loop)
        try:
            print("Starting event loop, server should run now...")
            self.loop.run_until_complete(self.server)
            self.loop.run_forever()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.loop.close()

    def run(self):
        self.thread = threading.Thread(target=self.start_server, daemon=True)
        self.thread.start()


if __name__ == '__main__':
    host = "192.168.178.123"
    port = settings.SERVER_PORT
    running = True
    ws_server = WebSocketServer(host, port)
    if ws_server.debug:
        print(f"Starting server on {host}:{port}")
    ws_server.run()
    while running:
        cmd = input("Enter command (start/stop/exit): ").strip().lower()
        if cmd == "stop":
            running = False
            print("Stopping server...")
            break
        else:
            print("Unknown command.")

    print("Server has shut down...")
