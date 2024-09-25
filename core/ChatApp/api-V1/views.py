from urllib import request
from click import group
from rest_framework import generics
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from ..models import (ChatGroup , GroupMessage , GroupMember)
from accounts.models import Profile
from .serializer import (GroupSerializer, MessageSerializer , ChatGroupSerializer )
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
        if 'name_group' in self.kwargs and self.kwargs['name_group'] is not None:
            group_name = self.kwargs['name_group']
            
            queryset = GroupMessage.objects.filter(group__name =group_name).all()
        else:
            queryset = {}
        return queryset

    def perform_create(self, serializer):
        author= Profile.objects.get(user=self.request.user)
        group_id = self.kwargs['pk']
        group_obj = ChatGroup.objects.get(id= group_id)
        serializer.save(author=author, group=group_obj)

    
# List all Grpups
class GroupListCreateView(generics.ListCreateAPIView):
    queryset = ChatGroup.objects.all()
    serializer_class = GroupSerializer
    


# render iNDEX Page
class IndexView(TemplateView):
    template_name = 'ChatApp/index.html'
    login_url = '/login/'

# render index html 
    
class loginView(TemplateView):
    template_name = 'ChatApp/login.html'   





# for listing all groups which request.user is member of these 

class UserGroupsListView(generics.ListAPIView):
    serializer_class = ChatGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
    
        group_obj = GroupMember.objects.filter(user = self.request.user)
        return group_obj      
    




