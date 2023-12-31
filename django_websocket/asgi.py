"""
ASGI config for django_websocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application

from utils.channel import CustomAuthSubProtocolMiddlewareStack
from websockets.urls import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_websocket.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": CustomAuthSubProtocolMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)