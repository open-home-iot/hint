from django.shortcuts import HttpResponse
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from backend.events.events import *
from backend.events.models import EventStatus


def event_alarm(req, alarm):
    print("Got the following alarm status: ", alarm)
    try:
        event_status = EventStatus.objects.get(pk=1)
        event_status.alarm = alarm == 'on'
        event_status.save()
    except ObjectDoesNotExist:
        EventStatus.objects.create(alarm=alarm == 'on')

    layer = get_channel_layer()
    async_to_sync(layer.group_send)('events', {
        'type': EVENT[PROXIMITY_ALARM],
        'content': alarm
    })
    return HttpResponse()


def get_event_status(req):
    alarm_status = False
    try:
        event_status = EventStatus.objects.get(pk=1)
        alarm_status = event_status.alarm
    except ObjectDoesNotExist:
        pass
    finally:
        return JsonResponse({'alarm': alarm_status})
