"""
ASGI config for Core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.urls import path, include
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from todo.consumer import todo_consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Core.settings")

#application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": URLRouter([
        path('todo', todo_consumer.as_asgi()) 

        ])
       
    }
)
