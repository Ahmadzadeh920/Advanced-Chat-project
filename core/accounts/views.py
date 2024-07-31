# from django.shortcuts import render


from rest_framework import generics
from .serializers import CustomUserSerializer
from .models import CustomUser

# Create your views here.
class CustomRegisterView(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset= CustomUser.objects.all()

