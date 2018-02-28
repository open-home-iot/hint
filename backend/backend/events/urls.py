from django.conf.urls import url

from backend.events.views import event_alarm, get_event_status


urlpatterns = [
    url(r'alarm/(?P<alarm>\w+)$', event_alarm),
    url(r'status/$', get_event_status)
]
