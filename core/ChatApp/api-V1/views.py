from rest_framework import generics
from django.shortcuts import get_object_or_404
from ..models import (ChatGroup , GroupMessage)
from .serializer import (GroupSerializer, MessageSerializer)
from rest_framework.permissions import (
    IsAuthenticated,
)






#retirive all messages related to one group 
class GroupMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    #permission_classes = [IsAuthenticated,]
   
    def get_queryset(self):
        # Override to retrieve only the messages for the specified group
        group_id = self.kwargs['pk']
        queryset = GroupMessage.objects.filter(group_id =group_id).all()
        return queryset

    