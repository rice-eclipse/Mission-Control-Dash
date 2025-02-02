import logo from './logo.svg';
import './App.css';
import dashInterface from "./dashInterface"
import { useState, useEffect, useRef} from 'react';

//display the data sent from the server
//create a button that when pressed, sends data to the server
function App() {

  const [driverCommands, setDriverCommands] = useState({});
  const dashboard = useRef();

  // Callback function to update state
  const updateDriverCommands = (newData) => {
    setDriverCommands(newData);
  };

  useEffect(() => {
    //passes in the callback funcion
    dashboard.current = new dashInterface(updateDriverCommands);
    return () => {
      if (dashboard.current?.client?.readyState === WebSocket.OPEN) {
          dashboard.current.closeConnection();
      }
  }
  }, []);

  const relayDriverData = () => {
    if (dashboard.current){
      dashboard.current.relayData();
    }
    else{
      console.log("connection not ready");
    }
  
  }
  return (
    <div className="App">
      <h1>Hi</h1>
      <button onClick={relayDriverData} disabled={!dashboard.current}>
        Send Current!
      </button>
      <pre>{JSON.stringify(driverCommands, null, 2)}</pre>
    </div>
  );

};
export default App;


