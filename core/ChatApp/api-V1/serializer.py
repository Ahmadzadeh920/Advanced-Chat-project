from rest_framework import serializers
from ..models import ChatGroup , GroupMessage
from accounts.models import Profile


class MessageSerializer(serializers.ModelSerializer):
    email_author = serializers.CharField(source="author.user.email", read_only=True)
    
    class Meta:
        model = GroupMessage
        fields = ['body','email_author', 'created' ]

class GroupSerializer(serializers.ModelSerializer):   
    
    class Meta:
        model = ChatGroup
        fields = ['id', 'name']  # 'id' is included by default 