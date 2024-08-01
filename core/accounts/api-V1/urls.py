from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView , TokenObtainPairView
app_name = "accounts"
urlpatterns = [
    path('register/',RegisterationApiview.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path( "activate/jwt/<str:token>", ActivationAccountJWT.as_view(), name="activation_account_jwt",),
   ]
