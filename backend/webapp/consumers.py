import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.conf import settings


class HumeConsumer(WebsocketConsumer):
    """Allows frontend users to subscribe to events related to a Home"""

    def __init__(self, *args, **kwargs):
        """"""
        self.hume_uuids = set()
        super().__init__(*args, **kwargs)

    def connect(self):
        """
        TODO On connection, accept the connection. Authentication checks should
         already have been made?
        """
        self.accept()

    def disconnect(self, close_code):
        """
        Not strictly necessary, but spares performance to discard the UUID
        group add on disconnect. If this is not done, or fails, the channel
        will be cleaned up after group_expiry seconds. See the CHANNEL_LAYER
        Django setting to find exactly what it is set to.
        """
        for hume_uuid in self.hume_uuids:
            async_to_sync(self.channel_layer.group_discard)(
                hume_uuid, self.channel_name
            )

    def receive(self, text_data=None, **kwargs):
        """
        Called on receiving an event from the socket connection. Currently, the
        only expected event is a subscription for a home ID.
        """
        if text_data == "get_connection_timeout_seconds":
            ges = settings.CHANNEL_LAYERS["default"]["CONFIG"]["group_expiry"]
            self.send(
                json.dumps({"connection_timeout_seconds": ges})
            )
            return

        if text_data == "ping":
            self.refresh_group_memberships()
            return

        decoded_data = json.loads(text_data)
        hume_uuid = decoded_data["hume_uuid"]

        self.monitor_new_hume_uuid(hume_uuid)

    def monitor_new_hume_uuid(self, hume_uuid):
        """
        Adds the input hume_uuid to the consumers list of monitored UUIDs.
        """
        self.hume_uuids.add(hume_uuid)
        async_to_sync(self.channel_layer.group_add)(
            hume_uuid, self.channel_name
        )

    def refresh_group_memberships(self):
        """
        Refreshes group memberships for the channel in question.
        """
        for hume_uuid in self.hume_uuids:
            async_to_sync(self.channel_layer.group_add)(
                hume_uuid, self.channel_name
            )

    def hume_event(self, event):
        """
        Called when an event occurs for a particular home through:

        async_to_sync(channel_layer.group_send)(
            "1337",  # This is the home id (group name)
            {
                "type": "home.event",  # Ensures the home_event def is called
                ...
            }
        )

        :param event: contains event information to be propagated to websocket
                      listener. Format of the event can be found in the
                      consumer_views module in the broker app
        :type event: dict
        """
        def format_event(event):
            """
            Formats an incoming event for dispatch to a websocket client.

            :param event: dict with event information
            :returns: formatted JSON string
            """
            event.pop("type")  # Remove type, it's always "hume.event"
            return json.dumps(event)

        self.send(format_event(event))
