from django.urls import path
from .consumers import *
from todo.consumer import todo_consumer

websocket_urlpatterns = [
    path("chatroom/<chatroom_id>/", ChatroomConsumer.as_asgi()),
    path('todo/', todo_consumer.as_asgi()),
   

    
]