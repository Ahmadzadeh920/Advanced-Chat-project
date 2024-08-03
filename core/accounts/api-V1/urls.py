from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView , TokenObtainPairView
app_name = "accounts"
urlpatterns = [
    path('register/',RegisterationApiview.as_view(), name='register'),
    path(
        "activate/jwt/<str:token>",
        ActivationAccountJWT.as_view(),
        name="activation_account_jwt",
    ),
    path('customized-login/', ObtainAuthToken_Customized.as_view(), name='login-customized'),
    path('customized-logout/', AuthDiscardedToken.as_view(), name='logout-customized'),
    path('customized-request-reset-pass/',RequestPasswordReset.as_view(), name='customized-request-reset-pass'),
    path("reset/pass/<str:token>/", ResetPassword.as_view(),name="Token_reset_password",),
    path("change_password/", ChangePasswordView.as_view(), name="auth_change_password"),


    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path( "activate/jwt/<str:token>", ActivationAccountJWT.as_view(), name="activation_account_jwt",),
    path( "profile/<int:id>/", ProfileAPIView.as_view(), name="profile_api_view",),
   ]
