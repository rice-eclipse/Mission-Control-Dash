from gpiozero import Button, LED
import busio
import board
from adafruit_ht16k33 import segments
import time


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

def driver_control() -> None:
    for i in range(3):
        for driver in drivers:
            #updates the state of the ignition driver
            if (driver == "Ignition"):
                driver["key_state"] = read_pin(driver["key_pin"])
                driver["btn_state"] = read_pin(driver["btn_pin"])

                #sends ignition command if both of the pins are high
                if (driver["key_state"] and driver["btn_state"]):
                    driver_commands["Ignition"]["ignite"] = 1

            #updates the state of the other drivers      
            else:
                driver["switch_state"] = read_pin(driver["switch_pin"])

                #sends a command if the valve state and the switch state are different
                if (driver["switch_state"] != driver["valve_state"]):
                    if (driver["switch_state"] == 1):
                        driver_commands[driver]["actuate"] = 1
                    else:
                        driver_commands[driver]["deactuate"] = 1
            send_commands()
            reset_command_states()
        time.sleep(3)

def reset_command_states(self) -> None:
        for driver in self.commands:
            for command in self.commands[driver]:
                self.commands[driver][command] = 0

def send_commands() -> None:
    print(driver_commands)

def receive_states() -> None:
    for i in range(3):
      pass  

#wrapping the reading of the pin in a separate function in case we migrate to a different
#python gpio library
def read_pin(pin: int) -> int:
    return int(Button(pin).is_pressed)
