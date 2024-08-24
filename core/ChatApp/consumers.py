from channels.generic.websocket import WebsocketConsumer
from click import group
from .models import ChatGroup , GroupMessage
from django.shortcuts import get_object_or_404
import json
from asgiref.sync import async_to_sync

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
        self.chatroom_obj = get_object_or_404(ChatGroup, id =self.chatroom_id) 
        self.chatroom_name= self.chatroom_obj['name']
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name, self.channel_name
        )
        self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name, self.channel_name
        )


    def receive(self, text_data=None, bytes_data=None):
        txt_data_json = json.loads(text_data)
        body = txt_data_json['body']
        message = GroupMessage.objects.create(body= body , author = self.user, group = self.chatroom_obj)
        context = json.dumps({
            'message' : message,
            'user' : self.user
        })
    
        self.send(text_data=context)
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )


