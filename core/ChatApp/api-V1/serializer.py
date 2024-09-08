from rest_framework import serializers
from ..models import ChatGroup , GroupMessage
from accounts.models import Profile


class MessageSerializer(serializers.ModelSerializer):
    email_author = serializers.CharField(source="author.user.email", read_only=True)
    is_author = serializers.SerializerMethodField()
    
    # this function recognize the which one of message is belonged to requset.user   
    def get_is_author(self, attrs):
        request = self.context.get('request')
        return attrs.author.user == request.user
    
    class Meta:
        model = GroupMessage
        fields = ['body','email_author', 'created','is_author' ]
        extra_kwargs = {
            'group': {'required': True}  # Ensure this field is required
        }
    
    def __init__(self, *args, **kwargs):
        # Check if 'context' is provided and if the request method is 'POST'
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request.method == 'POST':
            # Remove the special_field from the serializer fields if POST method
            self.fields.pop('is_author', None)

    

 # define serializer for groups in chat   

class GroupSerializer(serializers.ModelSerializer):   
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.id)
    

    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")
    class Meta:
        model = ChatGroup
        fields = [ 'group_name', "relative_url","absolute_url"]  # 'id' is included by default 