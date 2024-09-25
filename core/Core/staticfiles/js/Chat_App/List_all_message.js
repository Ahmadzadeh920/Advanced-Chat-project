$.ajax({
    url: 'http://127.0.0.1:8000/chat/api/v1/group/public4/',
    headers: {
        'Authorization': `Bearer ${window.localStorage.getItem('accessToken')}`
    },
    type: "GET", 
    tokenFlag: true,
    success: function (data) {
        for (var i = 0; i < data.length; i++) {
            if (data[i].is_author== true) {
                // Create the elements
                
                var rowDiv = $('<div>', { class: 'row justify-content-end text-right mb-4' });
                var colDiv = $('<div>', { class: 'col-auto' });
                var cardDiv = $('<div>', { class: 'card' });
                var cardBodyDiv = $('<div>', { class: 'card-body p-2' });
                
                // Create the paragraph and its contents
                var paragraph = $('<p>', { class: 'mb-1', text: ''+data[i].body+'' });
                
                // Create the flex container_message
                var flexDiv = $('<div>', { class: 'd-flex align-items-center text-sm opacity-6' });
                var icon = $('<i>', { class: 'far fa-clock mr-1', 'aria-hidden': 'true' });
                var smallText = $('<small>', { text: '4:31pm' });
                
                // Append the icon and small text to the flex div
                flexDiv.append(icon).append(smallText);
                
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
            } 
            else 
            {
                
                // Create the elements
                var rowDiv = $('<div>', { class: 'row justify-content-start mb-4' });
                var colDiv = $('<div>', { class: 'col-auto' });
                var cardDiv = $('<div>', { class: 'card' });
                var cardBodyDiv = $('<div>', { class: 'card-body p-2' });
                
                // Create the paragraph and its contents
                var paragraph = $('<p>', { class: 'mb-1', text: ''+data[i].body+'' });
                
                // Create the flex container_message
                var flexDiv = $('<div>', { class: 'd-flex align-items-center text-sm opacity-6' });
                var icon = $('<i>', { class: 'far fa-clock mr-1', 'aria-hidden': 'true' });
                var smallText = $('<small>', { text: ''+data[i].email_author+'' });
                var smalldate = $('<small>', { text: ''+data[i].created+'' });
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
            }
        } // end of for loop
    }, // end success
    error: handleAjaxError
}); // end ajax
