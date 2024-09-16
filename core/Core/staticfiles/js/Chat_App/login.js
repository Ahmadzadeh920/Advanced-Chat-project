

$("#login-form").submit(function (event) {
    event.preventDefault();
    let formData = new FormData();
    formData.append('email', $('#email').val().trim());
    formData.append('password', $('#password').val().trim());

    $.ajax({
        url: "http://127.0.0.1:8000/accounts/api/v1/login_customized/",
        type: "POST",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            // store tokens in localStorage
            if (data['access'] !== null){
            window.localStorage.setItem('refreshToken', data['refresh']);
            window.localStorage.setItem('accessToken', data['access']);
            window.localStorage.setItem('user_id', data['user_id']);
            window.localStorage.setItem('email', data['email']);
            $.ajax({
                url: 'http://127.0.0.1:8000/chat/api/v1/', // Replace with your protected API endpoint
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${window.localStorage.getItem('accessToken')}`
                },
                success: function(response) {
                    console.log('Protected data:', response);
                },
                error: function(error) {
                    console.error('Error fetching protected data:', error);
                    if (error.status === 401) {
                        // Handle unauthorized access (redirect to login)
                        //window.location.href = 'http://127.0.0.1:8000/chat/api/v1/';
                        console.log('Unauthorized User')
                    }
                }
            });    


           
        }
        },
        error: function (rs, e) {
            console.error(rs.status);
           alert(rs.responseText);
        }
    }); // end ajax
});


$("#logout-link").click(function (event) {
    event.preventDefault();
    window.localStorage.removeItem('refreshToken');
    window.localStorage.removeItem('accessToken');
    window.localStorage.removeItem('user_id');
    window.localStorage.removeItem('email');
    
    window.location.href = "login/";

});