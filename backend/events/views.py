from django.http import HttpResponse

from channels.layers import get_channel_layer

from surveillance.models import AlarmHistory

from asgiref.sync import async_to_sync


def alarm_off(req):
    layer = get_channel_layer()
    async_to_sync(layer.group_send)('events', {
        'type': 'event.alarm',
        'state': 'off'
    })
    return HttpResponse()


def alarm_on(req, date):
    history = AlarmHistory.create(date)
    history.save()

    layer = get_channel_layer()
    async_to_sync(layer.group_send)('events', {
        'type': 'event.alarm',
        'state': 'on'
    })
    return HttpResponse()
