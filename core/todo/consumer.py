from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

class todo_consumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("todo", self.channel_name)

    def receive(self, text_data = None, bytes_data = None):
        print(text_data)
        self.send('Thank you')
    def disconnect(self, close_code):
        pass
       