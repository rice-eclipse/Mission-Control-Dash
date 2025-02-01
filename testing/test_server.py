import asyncio
from websockets.asyncio.server import serve
import json
import time

driver_commands = {
    "driver_1" : {
        "actuate": 0,
        "deactuate": 0
    },
    "driver_2":{
        "actuate": 0,
        "deactuate": 0
    }
}

async def receive_messages(websocket):
    async for message in websocket:
            print(message)

async def handler(websocket):

    while (True):
        driver_commands["driver_1"]["actuate"] = input("actuate 1?: ")
        driver_commands["driver_1"]["deactuate"] = input("deactuate 1?: ")
        driver_commands["driver_2"]["actuate"] = input("actuate 2?: ")
        driver_commands["driver_2"]["deactuate"] = input("deactuate 2?: ")

        await websocket.send(json.dumps(driver_commands))
        

        asyncio.create_task(receive_messages(websocket))

        
        


async def main():
    async with serve(handler, "127.0.0.1", 8000):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())