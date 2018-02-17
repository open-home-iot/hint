from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class EchoConsumer(WebsocketConsumer):
    """

    """

    def connect(self):
        """

        :return:
        """
        async_to_sync(self.channel_layer.group_add)('events', self.channel_name)
        self.connect()

    def disconnect(self, code):
        """

        :param code:
        :return:
        """
        async_to_sync(self.channel_layer.group_discard)('events', self.channel_name)
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        """

        :param text_data:
        :param bytes_data:
        :return:
        """
        async_to_sync(self.channel_layer.group_send)(
            'events',
            {
                'type': 'event.message',
                'text': text_data
            }
        )

    def event_message(self, event):
        """

        :param event:
        :return:
        """
        self.send(text_data=event['text'])
