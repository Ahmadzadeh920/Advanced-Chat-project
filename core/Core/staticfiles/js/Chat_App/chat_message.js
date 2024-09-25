$(document).ready(function() {
    // actual JWT token
    let jwtToken = window.localStorage.getItem('accessToken'); 

    let roomName = 'public4'; // The room_name you want to connect to
    let ws = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/?token=${encodeURIComponent(jwtToken)}`);
    
   // Connection opened
   ws.onopen = function() {
    console.log('WebSocket connection established.');
};

// Listen for messages
ws.onmessage = function(event) {
    let response = JSON.parse(event.data);
    console.log('Message from server:', JSON.parse(response.message).data);
    //  display received messages in the chat window here
     // Create the elements
     var rowDiv = $('<div>', { class: 'row justify-content-start mb-4' });
     var colDiv = $('<div>', { class: 'col-auto' });
     var cardDiv = $('<div>', { class: 'card' });
     var cardBodyDiv = $('<div>', { class: 'card-body p-2' });
     
     // Create the paragraph and its contents
     var paragraph = $('<p>', { class: 'mb-1', text: ' '+JSON.parse(response.message).data+' ' });
     
     // Create the flex container_message
     var flexDiv = $('<div>', { class: 'd-flex align-items-center text-sm opacity-6' });
     var icon = $('<i>', { class: 'far fa-clock mr-1', 'aria-hidden': 'true' });
     var smallText = $('<small>', { text: 'you are is author' });
     var smalldate = $('<small>', { text: ''+Date.now()+'' });
     // Append the icon and small text to the flex div
     flexDiv.append(icon).append(smallText).append(smalldate);
     
     // Append the paragraph and flex div to the card body
     cardBodyDiv.append(paragraph).append(flexDiv);
     
     // Append the card body to the card
     cardDiv.append(cardBodyDiv);
     
     // Append the card to the column
     colDiv.append(cardDiv);
     
     // Append the column to the row
     rowDiv.append(colDiv);
     
     // Lastly, append the row to the container_message in the body
     $('#container_message').append(rowDiv);

};

// Handle errors
ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};

// Connection closed
ws.onclose = function(event) {
    console.log('WebSocket connection closed:', event);
};

// Handle the form submission to send a message
$('#chat-form').on('submit', function() {
    const messageInput = $('#message-input');
    const message = messageInput.val();

    if (message) {
        ws.send(JSON.stringify({ type: 'message', data: message }));
        messageInput.val(''); // Clear the input field after sending
    }
});
});