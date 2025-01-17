import asyncio
from gpiozero import Button, LED
from multiprocessing.resource_sharer import stop
from testing.hardware_testing import read_state
from websockets.asyncio.server import ServerConnection, serve
import json
from cmd_sending import CmdSender
from data_handling import DataHandler
import busio
import board
from adafruit_ht16k33 import segments
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
    },
    "OPS_Pneumatic":{
        "valve_current": 0,# Data from quonkboard
        "valve_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_address": 0x72, #Use Data from quonkboard to update
        "current_display_obj" : None,
        "led_pin": 24,
        "led_obj": 0,
        "switch_pin": 16,
        "switch_obj": 0
    },
    "Engine_Vent":{
        "valve_current": 0,# Data from quonkboard
        "valve_state": 0, #Use Data from quonkboard to update
        "switch_state": 0, # read switch on MC dashboard
        "current_display_address": 0x73, #Use Data from quonkboard to update
        "current_display_obj" : None,
        "led_pin": 25,
        "led_obj":0,
        "switch_pin": 17,
        "switch_obj": 0
    },
    "Ignition":{
        "key_state": 0, # read key state on MC dashboard
        "btn_state": 0,# read btn state on MC dashboard
        "key_pin": 4, 
        "key_obj": 0,
        "btn_pin": 26,
        "btn_obj": 0
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
    },
    "OPS_Pneumatic": {
        "actuate": 0,
        "deactuate": 0
    },
    "Engine_Vent":{
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
        #instantiates all the led and switch objects
        driver_pin =  "key_pin" if driver == "Ignition" else "switch_pin"
        driver_obj =  "key_obj" if driver == "Ignition" else "switch_obj"
        drivers[driver][driver_obj] = Button(drivers[driver][driver_pin])
        
        if driver == "Ignition":
            drivers[driver]["btn_obj"] = Button(drivers[driver]["btn_pin"])
        else:
            drivers[driver]["led_obj"] = LED(drivers[driver]["led_pin"])

        drivers[driver]["current_display_obj"] = segments.Seg7x4(i2c, address=
                                                                 drivers[driver]["current_display_address"])
        drivers[driver]["current_display_obj"].fill(0)
        ensure_state_off(driver)
        
#keeps looping until the operator turns the switch off
def ensure_state_off(driver: dict) -> None:
    #checks if the driver is a valve or ignition
    driver_obj =  "key_obj" if driver == "Ignition" else "switch_obj"
    while (read_state(drivers[driver][driver_obj])==1):
        #TODO: Some kind of alert mechanism
        time.sleep(0.1)
        

async def main():
    initiate()
    async with CmdSender(drivers, driver_commands) as cmd_sender:
        async def handler(websocket):
            await cmd_sender.send_command(websocket)

    #TODO: implement the stop signal
    stop_signal = asyncio.get_running_loop().create_future()

    async with serve(handler, "",8001):
        await stop_signal

#wrapping the reading of the pin in a separate function in case we migrate to a different
#python gpio library
def read_state(obj: Button) -> int:
    return int(Button(obj).is_pressed)


if __name__== "__main__":
    asyncio.run(main())