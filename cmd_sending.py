import asyncio
import asyncpio
from data_handling import DataHandler


#TODO: Pin definitions
IGNITION_BUTTON = 10
IGNITION_KEY = 20
VALVE1 = 0
VALVE2 = 1
VALVE3 = 3
VALVE4 = 4

ON = 1

class CmdSender:

    def __init__(self,drivers: dict, driver_commands: dict, data_handler:DataHandler)-> None:
        self.drivers = drivers,
        self.commands = driver_commands,
        self.data_handler = data_handler

    #Loops through each switch and checks if its state has been changed
    #sends the command to actuate/deactuate driver
    async def driver_control(self):
        await self.update_driver_states()
        for driver in self.drivers:
            if (driver == "Ignition"):
                driver["key_state"] = await self.read_pin(driver["key_pin"])
                driver["btn_state"] = await self.read_pin(driver["btn_pin"])

                #sends ignition command if both of the pins are high
                if (driver["key_state"] and driver["btn_state"]):
                    self.commands["Ignition"]["ignite"] = 1;
                    
            else:
                driver["switch_state"] = await self.read_pin(driver["switch_pin"]);
                if (driver["switch_state"] != driver["led_state"]):
                    if (driver["switch_state"] == 1):
                        self.commands[driver]["actuate"] = 1
                    else:
                        self.commands[driver]["deactuate"] = 1
        #send the message object
        await self.send_command()
        self.reset_commands()
    async def read_pin(pin: int, driver: str):
        driver["switch_state"] = await asyncpio.read_pin(pin)
        
