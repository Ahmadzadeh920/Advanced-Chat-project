from rest_framework import generics
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from ..models import (ChatGroup , GroupMessage)
from accounts.models import Profile
from .serializer import (GroupSerializer, MessageSerializer )
from rest_framework.permissions import (
    IsAuthenticated,
)
from django.views.generic import TemplateView
from django.shortcuts import render
from accounts.permissions import IsProfileCompleted
from rest_framework.views import APIView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

#retirive all messages related to one group 
class GroupMessagesView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsProfileCompleted]
    def get_queryset(self):
        # Override to retrieve only the messages for the specified group
        group_id = self.kwargs['pk']
        queryset = GroupMessage.objects.filter(group_id =group_id).all()
        return queryset

    def perform_create(self, serializer):
        author= Profile.objects.get(user=self.request.user)
        group_id = self.kwargs['pk']
        group_obj = ChatGroup.objects.get(id= group_id)
        serializer.save(author=author, group=group_obj)

    

class GroupListCreateView(generics.ListCreateAPIView):
    queryset = ChatGroup.objects.all()
    serializer_class = GroupSerializer
    



class IndexView(TemplateView):
    template_name = 'ChatApp/index.html'
    login_url = '/login/'

# render index html 

'''class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'ChatApp/index.html' '''
    
    
    
    
class loginView(TemplateView):
    template_name = 'ChatApp/login.html'   


# render login html 
'''class loginView(LoginView):
    template_name = 'ChatApp/login.html'
    success_url = reverse_lazy('home')  # Redirect to home after login
    '''
