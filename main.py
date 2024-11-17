import asyncio
from multiprocessing.resource_sharer import stop
from websockets.asyncio.server import ServerConnection, serve
import json
from cmd_sending import CmdSender
from data_handling import DataHandler
import pigpio
import time

#TODO: Pinout definitions (move to config too)

#TODO: clean this up and move to config file
drivers =  {
    "Engine_Vent": {
        "valve_current": 0, # Data from quonkboard
        "led_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_pin": 0, #Use Data from quonkboard to update
        "led_pin": 0, #output pin
        "switch_pin": 0

    },
    "Ground_Purge":{
        "valve_current": 0,# Data from quonkboard
        "led_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_pin": 0, #Use Data from quonkboard to update
        "led_pin": 0,
        "switch_pin": 0
    },
    "Isolation":{
        "valve_current": 0,# Data from quonkboard
        "led_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_pin": 0, #Use Data from quonkboard to update
        "led_pin": 0,
        "switch_pin": 0
    },
    "Ignition":{
        "key_state": 0, # read key state on MC dashboard
        "btn_state": 0,# read btn state on MC dashboard
        "key_pin": 0,
        "btn_pin": 0 
    }
}

driver_commands = {
    "Engine_Vent":{
        "actuate": 0,
        "deactuate": 0
    },
    "Ground_Purge": {
        "actuate": 0,
        "deactuate": 0
    },
    "Isolation": {
        "actuate": 0,
        "deactuate": 0
    },
    "Ignition": {
        "ignite": 0
    }
}
pi = pigpio.pi()

#Ensures all the valve switches are off to avoid accidental actuation on startup 
def initiate() -> None:
    for driver in drivers:
        ensure_state_off(driver)

#keeps looping until the operator turns the switch off
def ensure_state_off(driver: dict) -> None:
    #checks if the driver is a valve or ignition
    driver_pin =  "key_pin" if driver == "Ignition" else "switch_pin"
    while (read_pin(driver[driver_pin], driver)==1):
        #TODO: Some kind of alert mechanism
        time.sleep(0.1)
    driver["key_state"] = read_pin(driver["key_pin"], driver)

def read_pin(pin: int, driver: str):
        return pi.read_pin(pin)

async def main():
    initiate()

    async with CmdSender(drivers, driver_commands, pi) as cmd_sender:
        async def handler(websocket):
            await cmd_sender.add_client(websocket)

    #TODO: implement the stop signal
    stop_signal = asyncio.get_running_loop().create_future()

    async with serve(handler, "",5000):
        await stop_signal




if __name__== "__main__":
    asyncio.run(main())