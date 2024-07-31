from django.urls import path
from .views import *


urlpatterns = [
    path('register/', CustomRegisterView.as_view(), name='rest_register'),
   ]
