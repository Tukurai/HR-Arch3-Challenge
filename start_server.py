import sys
import os
from Server.server import WebSocketServer

print("TESTING")

if __name__ == "__main__":
    if os.getcwd() not in sys.path:
        print("Adding current directory to path")
        sys.path.insert(0,os.getcwd())
    else:
        print("Current directory already in path, continuing...")
    server = WebSocketServer()