# yourapp/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer

class MyConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        # You can process the received message here
        text_data_json = json.loads(text_data)

        # Echo the message back to the client
        self.send(text_data=json.dumps({
            'message': text_data_json['message']
        }))
