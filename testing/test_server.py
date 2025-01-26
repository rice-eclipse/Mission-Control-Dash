import asyncio
from websockets.asyncio.server import ServerConnection, serve
import json
import time

async def server():
    async def receive_command(websocket):
        for message in websocket:
            print("message")