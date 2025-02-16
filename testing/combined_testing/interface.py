from gpiozero import Button, LED
#import busiocd 
#import board
#from adafruit_ht16k33 import segments
import time
import json


# Ensures all the valve switches are off to avoid accidental actuation on startup 
# creates all the i2c objects for the 7 segment displays
"""
def initiate() -> None:
    i2c = busio.I2C(board.SCL, board.SDA)
    for driver in drivers:
        #instantiates all the led and switch objects
        driver_pin =  "key_pin" if driver == "Ignition" else "switch_pin"
        driver_obj =  "key_obj" if driver == "Ignition" else "switch_obj"
        drivers[driver][driver_obj] = Button(drivers[driver][driver_pin])
        
        if driver == "Ignition":
            drivers[driver]["btn_obj"] = Button(drivers[driver]["btn_pin"])

        drivers[driver]["current_display_obj"] = segments.Seg7x4(i2c, address=
                                                                 drivers[driver]["current_display_address"])
        drivers[driver]["current_display_obj"].fill(0)
        ensure_state_off(driver)
        
def receive_states() -> None:
    for i in range(3):
      pass  

"""

def gpio_test1() -> None:
    """
    Tests the reading of an input from a rocker switch and outputting a signal to an LED
    """
    #GPIO 17
    switch = Button(4, pull_up=True)
    led = LED(22)
    while (True):
        if (read_state(switch) == 1):
            print("on");
            led.on()
        else:
            led.off()
            print("off")
        time.sleep(3)

def initiate(drivers,driver_commands) -> None:
    for driver in drivers:
        #instantiates all the led and switch objects
        driver_pin =  "key_pin" if driver == "Ignition" else "switch_pin"
        driver_obj =  "key_obj" if driver == "Ignition" else "switch_obj"
        print(driver)
        drivers[driver][driver_obj] = Button(drivers[driver][driver_pin])
        if driver == "Ignition":
            drivers[driver]["btn_obj"] = Button(drivers[driver]["btn_pin"])
        
        
        print(drivers[driver][driver_obj])
    ensure_state_off(drivers)

#eplace with event handler that triggers when a switch is on
def ensure_state_off(drivers) -> None:
    #checks if the driver is a valve or ignition
    for driver in drivers:
        driver_obj =  "key_obj" if driver == "Ignition" else "switch_obj"
        while (read_state(drivers[driver][driver_obj])==1):
            print("turn off switch!")
            time.sleep(0.5)
    print("all switches off")
        
async def driver_control(websocket,drivers,driver_commands) -> None:
    for driver in drivers:
        #updates the state of the ignition driver
        if (driver == "Ignition"):
            drivers[driver]["key_state"] = read_state(drivers[driver]["key_obj"])
            drivers[driver]["btn_state"] = read_state(drivers[driver]["btn_obj"])

            #sends ignition command if both of the pins are high
            if (drivers[driver]["key_state"] and drivers[driver]["btn_state"]):
                driver_commands["Ignition"]["ignite"] = 1

        #updates the state of the other drivers      
        else:
            drivers[driver]["switch_state"] = read_state(drivers[driver]["switch_obj"])

            #sends a command if the valve state and the switch state are different
            if (drivers[driver]["switch_state"] != drivers[driver]["valve_state"]):
                if (drivers[driver]["switch_state"] == 1):
                    driver_commands[driver]["actuate"] = 1
                    driver_commands[driver]["deactuate"] = 0
                else:
                    driver_commands[driver]["deactuate"] = 1
                    driver_commands[driver]["actuate"] = 0
        print(driver_commands)
        await send_commands(websocket,driver_commands)
        drivers[driver]["valve_state"] = drivers[driver]["switch_state"]
        #reset_command_states(driver_commands)
    time.sleep(0.5)

def reset_command_states(driver_commands) -> None:
        for driver in driver_commands:
            for command in driver_commands[driver]:
                driver_commands[driver][command] = 0

async def send_commands(websocket, driver_commands) -> None:
    await websocket.send(json.dumps(driver_commands))
#wrapping the reading of the pin in a separate function in case we migrate to a different
#python gpio library
def read_state(obj: Button) -> int:
    return int(obj.is_pressed)

if __name__ == "__main__":
    #gpio_test1()
    initiate()