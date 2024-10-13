IGNITION_BUTTON = 10
IGNITION_KEY = 20
VALVE1 = 0
VALVE2 = 1
VALVE3 = 3
VALVE4 = 4

ON = 1

class Cmd_Sender:

    def __init__(self,valves):
        self.valves = valves
        
    def initiate(selfs):
        ensure_state_off(ignition_key)
        ensure_state_off(valve1)
        ensure_state_off(valve2)
        ensure_state_off(valve3)
        ensure_state_off(valve4)
        call_loop()
    
    #rename var 'elec'
    def ensure_state_off(self,elec):
        if(elec.isOn()):
            while(elec.isOn()):
                elec.led.on()
                sleep(1)
                elec.led.off()
                sleep(1)
            elec.led.off()
    
    