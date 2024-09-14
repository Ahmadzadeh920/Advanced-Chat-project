from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView , TokenObtainPairView ,TokenBlacklistView, TokenVerifyView
app_name = "accounts"
urlpatterns = [
    path('register/',RegisterationApiview.as_view(), name='register'),
    path("activate/jwt/<str:token>", ActivationAccountJWT.as_view(), name="activation_account_jwt",
    ),
   
    # this login with JWT
    path('customized-request-reset-pass/',RequestPasswordReset.as_view(), name='customized-request-reset-pass'),
    path("reset/pass/<str:token>/", ResetPassword.as_view(),name="Token_reset_password",),
    path("change_password/", ChangePasswordView.as_view(), name="auth_change_password"),

# this login with JWT
    path('login_customized/', CustimizedTokenObtainPairView.as_view(), name= 'login_jwt'),
    path('logout-jwt/', TokenBlacklistView.as_view(), name='token_blacklist'),
    
    path( "activate/jwt/<str:token>", ActivationAccountJWT.as_view(), name="activation_account_jwt",),
    path( "profile/", ProfileApiView.as_view(), name="profile_api_view",),
    path( "create_profile/",CreateProfileApiView.as_view(), name = "profile_create_api_view"),
    
# this is JWT with the library rest_framework_simplejwt.views
    path('token/create/', TokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
   ]
