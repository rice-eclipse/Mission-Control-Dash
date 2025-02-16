import asyncio
from gpiozero import Button, LED
from websockets.server import serve
import json
from interface import initiate, driver_control
import time

#TODO: Pinout definitions (move to config too)

#NOTE: THE PINS REFER TO THE GPIO PINS, NOT THE PHYSICAL PIN NUMBER!!!
drivers =  {
    "Oxidizer_Fill": {
        "valve_current": 0, # Data from quonkboard
        "valve_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_address": 0x70, #Use Data from quonkboard to update
        "current_display_obj" : None,
        "led_pin": 22, #output pin
        "led_obj": 0,
        "switch_pin": 20,
        "switch_obj": 0

    },
    "Ground_Vent":{
        "valve_current": 0,# Data from quonkboard
        "valve_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_address": 0x71, #Use Data from quonkboard to update
        "led_pin": 23,
        "led_obj": 0,
        "switch_pin": 6,
        "switch_obj": 0
    }
}


driver_commands = {
    "Oxidizer_Fill":{
        "actuate": 0,
        "deactuate": 0
    },
    "Ground_Vent": {
        "actuate": 0,
        "deactuate": 0
    }
}

async def receive_driver_current(websocket):
    try:
        message = await asyncio.wait_for(websocket.recv(),timeout=2)
        print(message)
        states = json.loads(message)
        for driver in drivers.keys():
                drivers[driver]["valve_current"] = states[driver]["valve_current"]
        
        print(drivers)
    except asyncio.TimeoutError:
        return
""""
async def send_messages(websocket):
    driver_commands["driver_1"]["actuate"] = input("actuate 1?: ")
    driver_commands["driver_1"]["deactuate"] = input("deactuate 1?: ")
    driver_commands["driver_2"]["actuate"] = input("actuate 2?: ")
    driver_commands["driver_2"]["deactuate"] = input("deactuate 2?: ")

    await websocket.send(json.dumps(driver_commands))
"""
async def handler(websocket):
    initiate(drivers,driver_commands)
    print("starting server")
    while (True):
        await driver_control(websocket, drivers, driver_commands)
        #await receive_driver_current(websocket)

async def main():
    async with serve(handler, "127.0.0.1", 8000):
        await asyncio.get_running_loop().create_future()


if __name__ == "__main__":
    asyncio.run(main())