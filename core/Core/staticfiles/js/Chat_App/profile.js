$(document).ready(function () {

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

})