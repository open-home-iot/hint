"""
This module defines handling for incoming hub (HUME) events.
"""
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rabbitmq_client import ConsumeOK


def incoming_message(message):
    """
    ! NOTE ! Avoid putting expensive operations here or this will become a
    bottleneck and a half. No database lookups allowed!

    :param message: message from the HINT master command queue
    :type message: bytes
    """
    if isinstance(message, ConsumeOK):
        return

    decoded_command = json.loads(message.decode('utf-8'))

    # Extract message fields.
    hume_uuid = decoded_command["uuid"]
    command_type = decoded_command["type"]
    content = decoded_command["content"]

    # Perform message-specific handling here...
    # ...

    # Dispatch message to websocket consumers.
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        hume_uuid,
        {
            # Setting the "type" field here will lead to hume_event being
            # invoked for consumers listening on the HUME's UUID group/topic.
            "type": "hume.event",
            "hume_uuid": hume_uuid,
            "event_type": command_type,
            "content": content
        }
    )
