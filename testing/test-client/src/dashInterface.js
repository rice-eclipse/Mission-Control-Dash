export default function  dashInterface(callback){
    const client = new WebSocket("ws://127.0.0:8000");

    client.onopen = () => {
        console.log('Dashboard connection established');
    };

    //Receive the command message from the server and transm
    client.onmessage = (event) => {
        
        const cmd_message = JSON.parse(event.data);
    
    }
}