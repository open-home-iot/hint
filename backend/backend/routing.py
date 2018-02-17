from channels.routing import ProtocolTypeRouter
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


application = ProtocolTypeRouter({
    # Empty for now
})


def send_to_group():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('events', {'type': 'event.alarm'})
