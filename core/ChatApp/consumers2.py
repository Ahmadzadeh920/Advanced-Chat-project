
from channels.generic.websocket import WebsocketConsumer
from click import group
from .models import ChatGroup , GroupMessage
from django.shortcuts import get_object_or_404
import json
from asgiref.sync import async_to_sync
import jwt 
import Core.envs.common as settings
from accounts.models import CustomUser , Profile
from rest_framework.exceptions import AuthenticationFailed



# this method analyze scope and return user object 
def get_user_scope(scope , obj_chat):
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
    async def connect(self):
    
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
    
        self.chatroom_obj = get_object_or_404(ChatGroup, name =self.chatroom_name) 
        self.user = get_user_scope(self.scope , obj_chat = self.chatroom_obj)
        
        self.chatroom_id = self.chatroom_obj.id
        # group_add allows channel to receive messages sent to the group
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_id, self.channel_name
        )
        await self.accept()

    def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

       


        '''
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_obj, self.channel_name
        )
'''
'''
    def receive(self, text_data=None, bytes_data=None):
        
        Prfile_obj = Profile.objects.get(user = self.user)
        message_obj = GroupMessage.objects.create(body= text_data , author = Prfile_obj, group = self.chatroom_obj)
        message = json.dumps({
            'text' : text_data,
            'user' : Prfile_obj.name,
        })

        event = {
            'type': 'message_handler',
            'message_id': message_obj.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )
        
    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessage.objects.get(id=message_id)
        context = {
            'message': message,
            'user': self.user,
            'chat_group': chatroom_obj
        }
        
        self.send(text_data=context)

'''

