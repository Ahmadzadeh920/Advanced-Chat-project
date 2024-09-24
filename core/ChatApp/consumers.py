# consumers.py

import json
import jwt 
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatGroup, GroupMember, GroupMessage
from django.contrib.auth.models import User
from channels.auth import login
import Core.envs.common as settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from accounts.models import CustomUser , Profile

class ChatGroupConsumer(WebsocketConsumer):
    def connect(self):
        # Get the JWT token from the URL parameters or headers
        self.user = self.get_user_from_jwt(self.scope)

        # Get the group name from URL
        self.group_name = self.scope['url_route']['kwargs']['group_name']

        # Check if the user is a member of the group
        if self.is_member(self.user, self.group_name):
            self.room_group_name = f'{self.group_name}'

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()
        else:
            self.close()  # User is not a member of the group, close connection

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        # Receive message from WebSocket
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save the message to the database
        group = ChatGroup.objects.get(group_name=self.group_name)
        GroupMessage.objects.create(
            group=group,
            author=self.user.profile,
            body=message
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )



    def chat_message(self, event):
        # Receive message from room group
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

    def get_user_from_jwt(self, scope):
        headers = scope['headers']
        Authorization_header = None
        # for finiding Authorization header
        for key, value in headers:
            if key == b'authorization':
                Authorization_header = value
                break
        print('scope is')
        print(scope['headers'])
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
        
        return user_obj

    
    
    
    
    
    
    def is_member(self, user, group_name):
        try:
            group = ChatGroup.objects.get(name=group_name)
            return GroupMember.objects.filter(group=group, user=user).exists()
        except ChatGroup.DoesNotExist:
            return False
