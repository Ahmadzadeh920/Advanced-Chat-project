
$(document).ready(function() {
    const form = $('#login-form');
  
    
    form.on('submit', function(event) {
        event.preventDefault();

        const username = $('#email').val();
        const password = $('#password').val();

        $.ajax({
            url: 'http://127.0.0.1:8000/accounts/api/v1/login_customized/', // Update the URL if needed
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                email: username,
                password: password
            }),
            success: function(data) {
                // Successfully received the token
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);
                localStorage.setItem('user_id', data.user_id);
                localStorage.setItem('email', data.email);
 
            },
            error: function(xhr) {
                const data = xhr.responseJSON;
                alert('Login failed: ' + data.detail);
            }
        });
    });
});