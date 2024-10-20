
#TODO: Pin definitions


IGNITION_BUTTON = 10
IGNITION_KEY = 20
VALVE1 = 0
VALVE2 = 1
VALVE3 = 3
VALVE4 = 4

ON = 1

class Cmd_Sender:

    def __init__(self,drivers: dict)-> None:
        self.drivers = drivers
        
    #Ensures all the valve switches are off to avoid accidental actuation on startup 
    def initiate(self) -> None:
        for driver in self.drivers():
            self.ensure_state_off(driver)
    
    #keeps looping until the operator turns the switch off
    def ensure_state_off(self, driver: dict) -> None:
        #implement the pin reading mechanism
        if "switch_state" in driver.values():
            while (self.read_pin(driver["switch_state"] == 1)):
                #TODO: Some kind of alert mechanism
                pass

        else:
            while (self.read_pin(driver["key_state"] == 1)):
                #TODO: Some kind of alert mechanism
                pass

    def driver_control(self, driver: dict) -> None:
        for driver in self.drivers():
            if "switch_state" in driver.values():
                if (self.read_pin(driver["switch_state"] == 1)):
                    current = driver["valve_current"]
                    if (current == 1):
                        driver["led_pin"] = 1

    def read_pin(pin: int) -> bool:
        pass
