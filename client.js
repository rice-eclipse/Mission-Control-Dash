//Simulates the websocket client in Quonkboard
const client = null;
try{
  client = new WebSocket("ws://127.0.0.1:8000");

}
catch(error){
  console.error("Failed to connect to dashboard", error);
}
//Send the valve states when quonkboard receives new data from labjack
client.onopen = () =>{
    const msg = {
      "Oxidizer_Fill": {
        "valve_current": 36
      },
      "Ground_Vent": {
        "valve_current": 48
      },
      "OPS_Pneumatic": {
        "valve_current":22
      },
      "Engine_Vent": {
        "valve_current": 17
      }     
    };

    client.send(JSON.stringify(msg));
};

// Receive commands and send to labjack
client.onmessage = (event) => {
  const driver_cmds = JSON.parse(event.data);

  for (const [key, value] of Object.entries(driver_cmds)){
    if (value.actuate == 1){
      console.log(`${key} is actuated`);
    }
    else{
      console.log(`${key} is deactuated`);
    }
  }
}