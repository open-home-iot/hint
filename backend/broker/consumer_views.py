"""
This module defines handling for incoming hub (HUME) events.
"""
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def incoming_command(command):
    """
    ! NOTE ! Avoid putting expensive operations here or this will become a
    bottleneck and a half. No database lookups allowed!

    :param command: message from the HINT master command queue
    :type command: bytes
    """
    decoded_command = json.loads(command.decode('utf-8'))

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str(decoded_command["uuid"]),
        {
            # Setting the "type" field here will lead to hume_event being
            # invoked for consumers listening on the HUME's UUID group.
            "type": "hume.event",
            "event_type": decoded_command["type"],
            "hume_uuid": decoded_command["uuid"],
            "content": decoded_command["content"]
        }
    )
