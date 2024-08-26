from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync
import jwt 
import Core.envs.common as settings
from accounts.models import CustomUser

import json

class todo_consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("todo", self.channel_name)

    def receive(self, text_data = None, bytes_data = None):
        #txt_data_json = json.loads(text_data)
        print(type(text_data))
        self.send('Thank you')
    def disconnect(self, close_code):
        pass
       