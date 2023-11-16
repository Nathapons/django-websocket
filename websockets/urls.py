from django.urls import re_path

from websockets.consumers import MyConsumer


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<document_id>\d+)//$", MyConsumer.as_asgi()),
]
