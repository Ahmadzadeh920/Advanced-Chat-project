


    // this ajax for getting data from profile of user
    $.ajax({
        url: 'http://127.0.0.1:8000/accounts/api/v1/profile/',
        headers: {
            'Authorization': `Bearer ${window.localStorage.getItem('accessToken')}`
        },
        type: "GET", 
        tokenFlag: true,
        success: function (data) {
            $('#link_img_profile').find('img').remove();
            $('#link_img_profile').prepend(`<img src="${data.profile_picture}">`);
            $('#link_img_profile img').css({
                'width': '80px',  // Changing the width
                'height':'80px',

                'opacity': '0.5',            // Changing the opacity
                'border-radius': '10px'      // Adding border radius
            });
            $("#name_profile").text(data.name);
            $("#email_profile").text(data.email);
            $("#lastname_profile").text(data.last_name);
            $("#title_role").text(data.role.title)
            $("#description_role").text(data.role.desc)

        },
        error: handleAjaxError
    }); // end ajax


// this ajax for getting data which list all groups which user is member of that
$.ajax({
    url: 'http://127.0.0.1:8000/chat/api/v1/user-groups/',
    headers: {
        'Authorization': `Bearer ${window.localStorage.getItem('accessToken')}`
    },
    type: "GET",
    tokenFlag: true,
    success: function (data) {
        if (Array.isArray(data)) { // Check if data is an array
            for(var i = 0; i < data.length; i++) {
                var item = data[i];
                

                // Group details
                var group = item.group || {}; // Ensure group exists
              
                // Create the elements
            var link = $('<a>', {
                href: "{% static 'javascript:;' %}",
                class: "d-block p-2"
            });

            var innerDiv = $('<div>', {
                class: "d-flex p-2"
            });

            var img = $('<img>', {
                alt: "Image",
                src: (group.img_group ? group.img_group : "http://127.0.0.1:8000/media/images_Group/no_img.png"),
                class: "avatar"
            });

            var contentDiv = $('<div>', {
                class: "ml-2"
            });

            var headerDiv = $('<div>', {
                class: "justify-content-between align-items-center"
            });

            var title = $('<h4>', {
                class: "mb-0 mt-1",
                html: '<span>'+group.name+'</span>'
            });

            var jobDescription = $('<p>', {
                class: "mb-0 text-xs font-weight-normal text-muted",
                
                html: '<span class="badge badge-success">'+ group.created_at+'</span>',
            });

            // Assemble the elements
            headerDiv.append(title);
            contentDiv.append(headerDiv).append(jobDescription);
            innerDiv.append(img).append(contentDiv);
            link.append(innerDiv);

            // Append to the container
            $('#container').append(link); //Change '#yourContainerId' to the ID of the container where you want to append it

            }
        } else {
            console.error("Expected an array but got:", data);
        }
    },
    error: handleAjaxError // Make sure this function is correctly defined
}); // end ajax



