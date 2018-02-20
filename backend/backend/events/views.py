from django.shortcuts import HttpResponse

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from backend.events.events import *


def alarm(req, alarm):
    print("Got the following alarm status: ", alarm)
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('events', {
        'type': EVENT[PROXIMITY_ALARM],
        'content': alarm
    })
    return HttpResponse('<p>Done</p>')
