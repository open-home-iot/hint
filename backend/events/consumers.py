from channels.generic.websocket import JsonWebsocketConsumer

from asgiref.sync import async_to_sync

from events.events import *


"""
INFO

* self.scope will contain much the same information as that you can find in a request object in a Django view.
* connect can raise AcceptConnection or DenyConnection exceptions
* In order to use groups for multicast messages you have to add a channel backend that is able to handle it. 
  RedisChannelLayer is one such handler, add it as BACKEND in settings.py in the var 
  CHANNEL_LAYERS['default']['BACKEND'].
* You can make a consumer automatically join a group upon connection by specifying the class variable groups. Groups
  has to be an iterable. The group will also be automatically dropped on disconnection.

"""


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
        self.send_json(
            {
                'type': EVENT[PROXIMITY_ALARM],
                'content': event['content']
            }
        )
