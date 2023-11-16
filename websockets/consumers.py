import re

from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer


class MyConsumer(JsonWebsocketConsumer):
    group_name = ''

    def connect(self):
        # Will work when socket connect
        self.user = self.scope['user']
        if not self.user.is_anonymous:
            email = re.sub("[@\.+]", "_", self.user.email)
            self.group_name = f'chat_{email}'
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, self.channel_name
            )
            self.accept("Bearer")
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        # Will work when socket send message
        user = self.scope['user']
        self.send_json({user.id: "Receive"})

    def disconnect(self, code):
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                    self.group_name, self.channel_name
            )
