import asyncio
from websockets.asyncio.server import serve
import json
import time
#from hardware_testing import initiate_gpio

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

drivers = {
     "Oxidizer_Fill": {
          "valve_current":0
     },
     "Ground_Vent": {
          "valve_current":0
     },
     "OPS_Pneumatic":{
          "valve_current": 0
     },
     "Engine_Vent":{
          "valve_current": 0
     }
}


async def receive_driver_current(websocket):
    try:
        message = await asyncio.wait_for(websocket.recv(),timeout=5)
        print(message)
        states = json.loads(message)
        for driver in drivers.keys():
                drivers[driver]["valve_current"] = states[driver]["valve_current"]
        
        print(drivers)
    except asyncio.TimeoutError:
        return

async def send_messages(websocket):
    driver_commands["driver_1"]["actuate"] = input("actuate 1?: ")
    driver_commands["driver_1"]["deactuate"] = input("deactuate 1?: ")
    driver_commands["driver_2"]["actuate"] = input("actuate 2?: ")
    driver_commands["driver_2"]["deactuate"] = input("deactuate 2?: ")

    await websocket.send(json.dumps(driver_commands))

async def handler(websocket):

    while (True):
        
        await send_messages(websocket)
        await receive_driver_current(websocket)

async def main():
    async with serve(handler, "127.0.0.1", 8000):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())