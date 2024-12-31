import asyncio
from gpiozero import Button, LED
from multiprocessing.resource_sharer import stop
from websockets.asyncio.server import ServerConnection, serve
import json
from cmd_sending import CmdSender
from data_handling import DataHandler
import busio
import board
from adafruit_ht16k33 import segments
import time

#TODO: Pinout definitions (move to config too)

#TODO: clean this up and move to config file
drivers =  {
    "Oxidizer_Fill": {
        "valve_current": 0, # Data from quonkboard
        "valve_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_address": 0x70, #Use Data from quonkboard to update
        "current_display_obj" : None,
        "led_pin": 22, #output pin
        "switch_pin": 5

    },
    "Ground_Vent":{
        "valve_current": 0,# Data from quonkboard
        "valve_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_address": 0x71, #Use Data from quonkboard to update
        "led_pin": 23,
        "switch_pin": 6
    },
    "OPS_Pneumatic":{
        "valve_current": 0,# Data from quonkboard
        "valve_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_address": 0x72, #Use Data from quonkboard to update
        "current_display_obj" : None,
        "led_pin": 24,
        "switch_pin": 16
    },
    "Engine_Vent":{
        "valve_current": 0,# Data from quonkboard
        "valve_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_address": 0x73, #Use Data from quonkboard to update
        "current_display_obj" : None,
        "led_pin": 25,
        "switch_pin": 17
    },
    "Ignition":{
        "key_state": 0, # read key state on MC dashboard
        "btn_state": 0,# read btn state on MC dashboard
        "key_pin": 0, 
        "btn_pin": 26 
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



# Ensures all the valve switches are off to avoid accidental actuation on startup 
# creates all the i2c objects for the 7 segment displays
def initiate() -> None:
    i2c = busio.I2C(board.SCL, board.SDA)
    for driver in drivers:
        drivers[driver]["current_display_obj"] = segments.Seg7x4(i2c, address=
                                                                 drivers[driver]["current_display_address"])
        drivers[driver]["current_display_obj"].fill(0)
        ensure_state_off(driver)
        
#keeps looping until the operator turns the switch off
def ensure_state_off(driver: dict) -> None:
    #checks if the driver is a valve or ignition
    driver_pin =  "key_pin" if driver == "Ignition" else "switch_pin"
    while (read_pin(driver[driver_pin])==1):
        #TODO: Some kind of alert mechanism
        time.sleep(0.1)
        
    #should be 0
    driver["key_state"] = read_pin(driver[driver_pin])


async def main():
    initiate()
    async with CmdSender(drivers, driver_commands, pi) as cmd_sender:
        async def handler(websocket):
            await cmd_sender.send_command(websocket)

    #TODO: implement the stop signal
    stop_signal = asyncio.get_running_loop().create_future()

    async with serve(handler, "",5000):
        await stop_signal

#wrapping the reading of the pin in a separate function in case we migrate to a different
#python gpio library
def read_pin(pin: int) -> int:
    return int(Button(pin).is_pressed)


if __name__== "__main__":
    asyncio.run(main())