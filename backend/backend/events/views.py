from django.shortcuts import HttpResponse

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync


def alarm(req):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('events', {
        'type': 'events.alarm',
        'content': 'triggered'
    })
    return HttpResponse('<p>Done</p>')
