"""
ASGI config for Core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.urls import path, include
from channels.routing import ProtocolTypeRouter, URLRouter
from ChatApp.chat_config.jwt_middleware import JWTAuthMiddleware

from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from ChatApp import  routing as routing_chat


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Core.envs.development")

#application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": 
        JWTAuthMiddleware(
            URLRouter(
                routing_chat.websocket_urlpatterns  # Update with your URL routing
           
        )
    ),
})