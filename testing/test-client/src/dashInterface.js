
/**
 * Dash Interface Class
 * Creates a WebSocket Client to manage the communication between the Dashboard 
 * computer and Quonkboard
 * @class
 * @param {function} updateDisplay- The callback function to update the Displa whenever a new message is recevied
   
 }}
 * @return {dashInterface} The dashInterface object
 */

/**
 * Connection should be created as soon as quonkboard initializes
 *  - useEffect in App.js that creates an instance of dashInterface
 */
class dashInterface{
/**
 * @constructor
 * @property {Socket} dashClient - The websocket client
 * @property {Object} driverCommands - The commands to actuate/2deactuate each valve and the ignition system
 * @property {Object} driverStates - The states of each valve taken from Interface
 */

    constructor (updateDisplay) {
        this.driverCommands = {};
        this.driverStates = {};
        
        this.client = new WebSocket('ws://127.0.0.1:8000');
        this.client.onopen = () =>{
            console.log("connected to the dashboard");
            
        };

        this.client.onmessage = (event) => {
            if (event.data == null){
                return;
            }

            else{
                const data = JSON.parse(event.data);
                // Stores the commands in the driver commands object.
                this.driverCommands =  data;
            }

            //used to update the main display when new commands arrive
            if (updateDisplay){
                updateDisplay(this.driverCommands);
            }
        };
    }

    closeConnection(){
        this.client.close();
    }

    //Whenever the send button is pressed, the driver currents should be sent over
    relayData(){
        if (this.client.readyState === WebSocket.OPEN){
            this.client.send(
                JSON.stringify({
                    "Oxidizer_Fill": {
                         "valve_current":1
                    },
                    "Ground_Vent": {
                         "valve_current":1
                    },
                    "OPS_Pneumatic":{
                         "valve_current": 1
                    },
                    "Engine_Vent":{
                         "valve_current": 1
                    }
               })
            );
            console.log("sent");
        }
        else if (this.client.readyState === WebSocket.CONNECTING){
            console.log("still connecting");
            //setInterval(() => this.relayData(),1000);
        }
        
    }

}
export default dashInterface;