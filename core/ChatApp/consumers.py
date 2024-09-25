# consumers.py

from email import message
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
from accounts.models import Profile, CustomUser





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
        
        profile_obj = Profile.objects.get(user = self.user)
        # Receive message from WebSocket
        #text_data_json = json.loads(text_data)
        
        # text data is string
        message = text_data
        # Save the message to the database
        group_obj = ChatGroup.objects.get(name=self.group_name)
        GroupMessage.objects.create(
            group=group_obj,
            author=profile_obj,
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
        
        # Check if the Authorization_header is not None
        if Authorization_header is not None:
            # Decode the header and split to get the access token
            access_token = Authorization_header.decode('utf-8').split()[1] 
        else:
            # Handle the case where Authorization_header is None
            # Assuming you're trying to get the token from query string
            query_string = self.scope.get('query_string', b'').decode('utf-8')
            
            # Make sure to check if there is a 'token=' in the query string
            if 'token=' in query_string:
                access_token = query_string.split('token=')[1]
            else:
                access_token = None  # or handle the case where no token is found
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
            group = ChatGroup.objects.get(name=self.group_name)
            return GroupMember.objects.filter(group=group, user=user).exists()
        except ChatGroup.DoesNotExist:
            return False
