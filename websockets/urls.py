from django.urls import re_path

from websockets.consumers import MyConsumer


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", MyConsumer.as_asgi()),
]
