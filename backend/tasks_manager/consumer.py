import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class NotificationConsumer(WebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'notifications',
            self.channel_name
        )

        print(f'-------------> Connected: {self.channel_name}')
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'notifications',
            self.channel_name
        )
        pass

    def receive(self, text_data):
        print('-------------> Recieve')

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'message': message
            }
        )

    def send_notification(self, event):
        message = event['message']
        print(f'-------------> Sending message: {message}')
        self.send(text_data=json.dumps({
            'message': message
        }))
