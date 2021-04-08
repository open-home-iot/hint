"""
This module defines handling for incoming hub (HUME) events.
"""
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def incoming_command(command):
    """
    :param command: message from the HINT master command queue
    :type command: bytes
    """
    print(command)
    decoded_command = json.loads(command.decode('utf-8'))

    try:
        # Needed to be put here since this function is imported at
        # AppConfig.ready, and at that point apps are not loaded yet.
        from backend.home.models import Home
        home = Home.objects.get(hume__uuid=decoded_command["uuid"])
    except Home.DoesNotExist:
        print("Tried to send home event for a hume that does not have a home")
        return

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(home.id),
        {
            "type": "home.event",  # Will lead to home_event being called
            "event_type": decoded_command["type"], #TODO Maybe change to eventType or messageType
            "home_id": home.id,
            "hume_uuid": decoded_command["uuid"],
            "content": decoded_command["content"]
        }
    )
