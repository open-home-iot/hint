from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync


class HumeConsumer(JsonWebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self):
        pass

    def receive(self, data):
        self.send(data=data)


class EventConsumer(JsonWebsocketConsumer):

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'events',
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            'events',
            self.channel_name
        )
        self.close()

    def receive_json(self, content, **kwargs):
        print("Received event: {}".format(content))
        self.send_json(content)

    # ------------------------------------------------------------------------------------------------------------------
    # Handler definitions! handlers will accept their corresponding message types. A message with type event.alarm
    # has to have a function event_alarm
    # ------------------------------------------------------------------------------------------------------------------

    def event_alarm(self, event):
        self.send_json(event)
