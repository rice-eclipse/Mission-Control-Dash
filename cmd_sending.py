import asyncio
import asyncpio
from data_handling import DataHandler
import json


#TODO: Pin definitions
IGNITION_BUTTON = 10
IGNITION_KEY = 20
VALVE1 = 0
VALVE2 = 1
VALVE3 = 3
VALVE4 = 4

VALVE_THRESHOLD = 0.5
ON = 1
OFF = 0

class CmdSender:

    def __init__(self,drivers: dict, driver_commands: dict, client = None)-> None:
        self.drivers = drivers
        self.commands = driver_commands
        self.client = client

    #Loops through each switch and checks if its state has been changed
    #sends the command to actuate/deactuate driver
    async def driver_control(self):
        await self.received_states()
        self.update_drivers()
        for driver in self.drivers:
            if (driver == "Ignition"):
                driver["key_state"] = await self.read_pin(driver["key_pin"])
                driver["btn_state"] = await self.read_pin(driver["btn_pin"])

                #sends ignition command if both of the pins are high
                if (driver["key_state"] and driver["btn_state"]):
                    self.commands["Ignition"]["ignite"] = 1
                    
            else:
                driver["switch_state"] = await self.read_pin(driver["switch_pin"]);
                if (driver["switch_state"] != driver["led_state"]):
                    if (driver["switch_state"] == 1):
                        self.commands[driver]["actuate"] = 1
                    else:
                        self.commands[driver]["deactuate"] = 1
        #send the message object
        await self.send_command()

    async def read_pin(pin: int, driver: str):
        driver["switch_state"] = await asyncpio.read_pin(pin)
        

    async def recieve_states(self):
        if self.client == None:
            await asyncio.sleep(0.1)

        message = await self.client.recv()
        states = json.load(message)
        
        for key in ["Engine_Vent", "Ground_Purge", "Isolation"]:
            current = states[key]["valve_current"]
            self.drivers[key]["valve_current"] = current
            
            if current > VALVE_THRESHOLD:
                self.drivers[key]['led_pin'] = ON
            else:
                self.drivers[key]['led_pin'] = OFF
            
            self.write_pin(self.drivers[key]['current_display_pin'], current)

    # TODO: implement wrapper for read_pin
    def read_pin(pin: int, driver: str):
        pass
    
    # TODO: implement write_pin
    def write_pin(pin: int, val: int):
        pass