// Example using jQuery
$(document).ready(function () {
    const group_name = "public4";  // replace with your group name
    const wsScheme = window.location.protocol === "https:" ? "wss" : "ws"; // Use wss on HTTPS
    const token = localStorage.getItem('accessToken'); // Retrieve your JWT token from storage
    const wsUrl = 'ws://localhost:8000/ws/chat/'+group_name+'/'; // Replace with your actual WebSocket URL
    
    // Initialize WebSocket connection
    const socket = new WebSocket(wsUrl, [], {
        headers: {
            'Authorization': `Bearer ${token}` // Attach the token
        }
    });





    // Set up event handlers
        socket.onopen = function(event) {
            
            console.log("WebSocket is open now.");
        };


    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        console.log(data.message);  // handle incoming message
    };

    $('#send-message-btn').on('click', function () {
        const message = $('#message-input').val();

        if (message) {
            socket.send(JSON.stringify({
                'message': message
            }));
            $('#message-input').val('');  // Clear input
        }
    });
});
