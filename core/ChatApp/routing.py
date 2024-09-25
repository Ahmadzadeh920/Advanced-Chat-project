from django.urls import re_path , path
from .consumers import ChatGroupConsumer
from todo.consumer import todo_consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<group_name>\w+)/$', ChatGroupConsumer.as_asgi()),
   
   

    
]