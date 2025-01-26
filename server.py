#!/usr/bin/env python

"""Echo server using the asyncio API."""

import asyncio
from websockets.asyncio.server import serve


async def handler(websocket):
    async for message in websocket:
        print(message)

    connected = {websocket}
    
    for connection in connected:
        connection.send("Message Recieved")


async def main():
    async with serve(handler, "127.0.0.1", 8000) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())