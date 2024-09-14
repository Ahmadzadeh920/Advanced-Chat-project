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
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


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
    


# render index html 
@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = 'ChatApp/index.html'
    permission_classes = [IsAuthenticated]
    
    


# render login html 
class loginView(TemplateView):
    template_name = 'ChatApp/login.html'
    