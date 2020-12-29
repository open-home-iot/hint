import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


"""
This module defines handling for incoming hub (HUME) events.
"""


def incoming_command_queue_message(message):
    """
    :param message: message from the HINT master command queue
    :type message: bytes
    """
    print(message)
    decoded_message = json.loads(message.decode('utf-8'))

    try:
        # Needed to be put here since this function is imported at
        # AppConfig.ready, and at that point apps are not loaded yet.
        from backend.home.models import Home
        home = Home.objects.get(hume__uuid=decoded_message["uuid"])
    except Home.DoesNotExist:
        print("Tried to send home event for a hume that does not have a home")
        return

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(home.id),
        {
            "type": "home.event",  # Will lead to home_event being called
            "home_id": home.id,
            "hume_uuid": decoded_message["uuid"],
        }
    )
