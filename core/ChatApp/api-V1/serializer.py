from rest_framework import serializers
from ..models import ChatGroup , GroupMessage , GroupMember
from accounts.models import Profile



# this class fro serializer massage

class MessageSerializer(serializers.ModelSerializer):
    email_author = serializers.CharField(source="author.user.email", read_only=True)
    is_author = serializers.SerializerMethodField()
    group_name = serializers.CharField(source="group.name", read_only=True)
    
    # this function recognize the which one of message is belonged to requset.user   
    def get_is_author(self, attrs):
        request = self.context.get('request')
        return attrs.author.user == request.user
    
    class Meta:
        model = GroupMessage
        fields = ['body','email_author', 'created','is_author','group_name' ]
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
        fields = [ 'name', "relative_url","absolute_url", "img_group"]  # 'id' is included by default 



# this serializer for Group memeber models

class ChatGroupSerializer(serializers.ModelSerializer):
    group = GroupSerializer()  # This will embed group information
    class Meta:
        model = GroupMember
        fields =['id', 'group', 'user']  # Specify fields you want to serialize