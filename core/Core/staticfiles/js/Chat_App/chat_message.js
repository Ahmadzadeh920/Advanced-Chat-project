$(document).ready(function() {
    // Replace with your actual JWT token
    let jwtToken = window.localStorage.getItem('accessToken'); 
    let ws = `ws://localhost:8000/ws/chat/public4/?token=${encodeURIComponent(jwtToken)}`;
    
    // Connection opened
    ws.onopen = function() {
        console.log('WebSocket connection established');
        // Send a message to the server
        ws.send(JSON.stringify({ type: 'message', data: 'Hello Server!' }));
    };

    // Listen for messages
    ws.onmessage = function(event) {
        let response = JSON.parse(event.data);
        console.log('Message from server:', response);
    };

    // Handle errors
    ws.onerror = function(error) {
        console.error('WebSocket error:', error);
    };

    // Connection closed
    ws.onclose = function(event) {
        console.log('WebSocket connection closed:', event);
    };
});
