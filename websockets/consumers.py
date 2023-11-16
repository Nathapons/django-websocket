import json

from channels.generic.websocket import JsonWebsocketConsumer

class MyConsumer(JsonWebsocketConsumer):

    def connect(self):
        # Will work when socket connect
        self.user = self.scope['user']
        if not self.user.is_anonymous:
            self.accept("Bearer")
            self.send_json({self.user.id: 'Connect'})
        else:
            self.close()

    def receive_json(self, content, **kwargs):
        # Will work when socket send message
        user = self.scope['user']
        self.send_json({user.id: "Receive"})
