$(document).ready(function () {
    /*
        Hitting an API endpoint, By sending access token in header of an API request
    */
    $.ajax({
        url: 'http://127.0.0.1:8000/chat/api/v1/',
        headers: {
            'Authorization': `Bearer ${window.localStorage.getItem('accessToken')}`
        },
        type: "GET",
        tokenFlag: true,
        success: function (data) {
            console.log('try to');
          

        },
        error: handleAjaxError
    }); // end ajax
});

function handleAjaxError(rs, e) {
    /*
        And if it returns 401, then we call obtainAccessTokenWithRefreshToken() method 
        To get a new access token using refresh token.
    */
    if (rs.status == 401) {
        if (this.tokenFlag) {
            this.tokenFlag = false;
            if (obtainAccessTokenWithRefreshToken()) {
                this.headers["Authorization"] = `Bearer ${window.localStorage.getItem('accessToken')}`
                $.ajax(this);  // calling API endpoint again with new access token
            }
        }
    } else {
        console.error(rs.responseText);
    }
}

function obtainAccessTokenWithRefreshToken() {
    /*
        This method will create new access token by using refresh token.
        If refresh token is invalid it will redirect user to login page
    */
    let flag = true;
    let formData = new FormData();
    formData.append('refresh', window.localStorage.getItem('refreshToken'));
    $.ajax({
        url: 'http://127.0.0.1:8000/accounts/api/v1/token/refresh/',
        type: "POST",
        data: formData,
        async: false,
        cache: false,
        processData: false,
        contentType: false,
        success: function (data) {
            window.localStorage.setItem('accessToken', data['access']);
        },
        error: function (rs, e) {
            if (rs.status == 401) {
                flag = false;
                window.localStorage.removeItem('refreshToken');
                window.localStorage.removeItem('accessToken');
                window.location.href = "/login/";
            } else {
                console.error(rs.responseText);
            }
        }
    }); // end ajax
    return flag
}