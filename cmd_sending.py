import asyncio
from typing import Self
from main import drivers
from gpiozero import LED, Button
import busio
import board
from adafruit_ht16k33 import segments
import json

#minimum current needed to open a valve
VALVE_THRESHOLD = 1

class CmdSender:

    def __init__(self,drivers: dict, driver_commands: dict, client = None)-> None:
        self.drivers = drivers
        self.commands = driver_commands
        self.client = client


    def __aenter__(self):
        self.driver_control()
        return self
    #Loops through each switch and checks if its state has been changed
    #sends the command to actuate/deactuate driver
    async def driver_control(self) -> None:
        await self.receive_states()
        for driver in self.drivers:
            #updates the state of the ignition driver
            if (driver == "Ignition"):
                self.drivers[driver]["key_state"] = self.read_state(self.drivers[driver]["key_obj"])
                self.drivers[driver]["btn_state"] = self.read_state(self.drivers[driver]["btn_obj"])

                #sends ignition command if both of the pins are high
                if (self.drivers[driver]["key_state"] and self.drivers[driver]["btn_state"]):
                    self.commands["Ignition"]["ignite"] = 1

            #updates the state of the other drivers      
            else:
                self.drivers[driver]["switch_state"] = self.read_state(self.drivers[driver]["switch_obj"])

                #sends a command if the valve state and the switch state are different
                if (self.drivers[driver]["switch_state"] != self.drivers[driver]["valve_state"]):
                    if (self.drivers[driver]["switch_state"] == 1):
                        self.commands[driver]["actuate"] = 1
                    else:
                        self.commands[driver]["deactuate"] = 1
        #send the message object
        await self.send_command()
        self.reset_command_states()

    def read_state(obj: Button) -> int:
       return int(Button(obj).is_pressed)
        

    async def recieve_states(self) -> None:
        while self.client == None:
            await asyncio.sleep(0.1)

        message = await self.client.recv()
        states = json.load(message)

        for key in drivers.key():
            current = states[key]["valve_current"]
            self.drivers[key]["valve_current"] = current
            self.display_current(self.drivers[key]["current_display_obj"], current)
            
            #turns on the led if the current is more than the threshold
            if current > VALVE_THRESHOLD:
                self.drivers[key]['led_pin'] = 0
                self.write_led(self.drivers[key]['led_obj'], 0)
            else:
                self.drivers[key]['led_pin'] = 1
                self.write_led(self.drivers[key]['led_obj'], 1)

    async def send_command(self) -> None:
        while self.client == None:
            await asyncio.sleep(0.1)
        self.client.send(json.dumps(self.driver_commands))
    
    async def add_client(self, client) -> None:
        self.client = client
    
    def write_led(self,obj: LED, val: int) -> None:
        if (int == 1):
            obj.on()
        else:
            obj.off()

    def reset_command_states(self) -> None:
        for driver in self.commands:
            for command in self.commands[driver]:
                self.commands[driver][command] = 0
    
    def display_current(self, display_obj, current) -> None:
        display_obj.fill(0)
        display_obj.print(current)
        