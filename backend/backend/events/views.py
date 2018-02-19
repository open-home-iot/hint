from django.shortcuts import HttpResponse

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from backend.events.events import *


def alarm(req):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('events', {
        'type': EVENT[PROXIMITY_ALARM],
        'content': EVENT_SUB_CAUSE[ON]
    })
    return HttpResponse('<p>Done</p>')
