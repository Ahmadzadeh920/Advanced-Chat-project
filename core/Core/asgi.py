"""
ASGI config for Core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.urls import path, include
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from ChatApp import  routing as routing_chat
from todo import routing as routing_todo

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Core.envs.development")

#application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
         "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                 
                    routing_chat.websocket_urlpatterns,
                
            )
        )
    ),
    }
)
