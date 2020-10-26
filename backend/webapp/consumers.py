from channels.generic.websocket import WebsocketConsumer


class HumeConsumer(WebsocketConsumer):

    def connect(self):
        print("Connected to HumeConsumer")
        print(self.scope["type"])
        self.accept()

    def disconnect(self, close_code):
        pass

    # Echoes
    def receive(self, text_data):
        self.send(text_data=text_data)
