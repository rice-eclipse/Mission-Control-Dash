import logo from './logo.svg';
import './App.css';
//import dashInterface from "./dashInterface.js"
import { useState, useEffect} from 'react';

//display the data sent from the server
//create a button that when pressed, sends data to the server
function App() {

  const [driverState, setDriverState] = useState();
  const [client, setClient] = useState(null);
  
  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000"); 

    ws.onopen = () => {
      console.log("connected to the dashboard");
      setClient(ws);
    }

    ws.onmessage = (event) => {
      setDriverState(event.data);
    }
    ws.onerror = (error) =>{
      console.error("Connection error", error);
    }
    ws.onclose = () => {
      console.log("connection closed");
    }
  }, []);

  return (
    <div className="App">
      <h1>{driverState}</h1>
      <button onClick={() => client.send("message")}>
        Send message
      </button>
    </div>
  );

};
export default App;


