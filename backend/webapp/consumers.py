import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from backend.hume.models import Hume


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
        user = self.scope["user"]

        self.accept()
        if isinstance(user, AnonymousUser):
            self.disconnect()
            return

    def disconnect(self, close_code=1000):
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
        self.close(close_code)

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
        # IMPORTANT
        # Verify the consumer user owns the hub in question, do NOT allow
        # information leaks through the websocket consumer!
        if Hume.objects.filter(uuid=hume_uuid,
                               home__users__id=self.scope["user"].id).exists():
            self.hume_uuids.add(hume_uuid)
            async_to_sync(self.channel_layer.group_add)(
                hume_uuid, self.channel_name
            )
        else:
            # Websocket connection is up to no good, close it.
            self.disconnect()

    def refresh_group_memberships(self):
        """
        Refreshes group memberships for the channel in question.
        """
        for hume_uuid in self.hume_uuids:
            async_to_sync(self.channel_layer.group_add)(
                hume_uuid, self.channel_name
            )

    def hume_event(self, event: dict):
        """
        Called when an event occurs for a particular hume through:

        async_to_sync(channel_layer.group_send)(
            <UUID>,
            {
                "type": "hume.event",
                ...
            }
        )

        :param event: contains event information to be propagated to websocket
                      listener. Format of the event can be found in the
                      consumer_views module in the broker app
        """
        def format_event(dictionary):
            """
            Formats an incoming event for dispatch to a websocket client.

            :param dictionary: dict with event information
            :returns: formatted JSON string
            """
            dictionary.pop("type")  # Remove type, it's always "hume.event"
            return json.dumps(dictionary)

        self.send(format_event(event))
