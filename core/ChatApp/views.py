from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from .models import (ChatGroup , GroupMessage)
from accounts.models import Profile

from django.shortcuts import render
from accounts.permissions import IsProfileCompleted


def index(request):
    return render(request,'ChatApp/index.html')



def login(request):
    return render(request,'ChatApp/login.html')



       