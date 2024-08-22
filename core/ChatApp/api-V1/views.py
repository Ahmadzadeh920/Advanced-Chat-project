from rest_framework import generics
from django.shortcuts import get_object_or_404
from ..models import (ChatGroup , GroupMessage)
from accounts.models import Profile
from .serializer import (GroupSerializer, MessageSerializer)
from rest_framework.permissions import (
    IsAuthenticated,
)


from accounts.permissions import IsProfileCompleted



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

    