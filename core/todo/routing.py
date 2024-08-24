from django.urls import path
from .consumer import *

websocket_urlpatterns = [
   
    path("todo_consumer/", todo_consumer.as_asgi()),

   
]