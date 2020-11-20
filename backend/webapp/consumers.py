from channels.generic.websocket import WebsocketConsumer


class HumeConsumer(WebsocketConsumer):

    def connect(self):
        print("Connected to HumeConsumer")

        # Get data from the URL route like so:
        print(self.scope["url_route"]["kwargs"]["hume_id"])

        self.accept()

    def disconnect(self, close_code):
        pass

    # Echoes
    def receive(self, text_data):
        self.send(text_data=text_data)
