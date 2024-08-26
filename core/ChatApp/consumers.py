
from channels.generic.websocket import WebsocketConsumer
from click import group
from .models import ChatGroup , GroupMessage
from django.shortcuts import get_object_or_404
import json
from asgiref.sync import async_to_sync
import jwt 
import Core.envs.common as settings
from accounts.models import CustomUser , Profile



# this method analyze scope and return user object 
def get_user_scope(scope):
    headers = scope['headers']
    Authorization_header = None
    # for finiding Authorization header
    for key, value in headers:
        if key == b'authorization':
            Authorization_header = value
            break
    access_token = Authorization_header.decode('utf-8').split( )[1]
    try:
        # Decode the JWT token
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get('user_id')  # Assuming user_id is stored in the token
        user_obj = CustomUser.objects.get(id=user_id)
            
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Token has expired')
    except jwt.DecodeError:
        raise AuthenticationFailed('Error decoding token')
    except User.DoesNotExist:
        raise AuthenticationFailed('No such user')
    return(user_obj)



class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = get_user_scope(self.scope)
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        self.chatroom_obj = get_object_or_404(ChatGroup, id =self.chatroom_id) 
        self.chatroom_name= self.chatroom_obj.group_name
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )


    def receive(self, text_data=None, bytes_data=None):
        
        Prfile_obj = Profile.objects.get(user = self.user)
        message = GroupMessage.objects.create(body= text_data , author = Prfile_obj, group = self.chatroom_obj)
        context = json.dumps({
            'message' : text_data,
            'user' : self.user
        })
    
        self.send(text_data=context)
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )


