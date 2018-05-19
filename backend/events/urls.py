from django.urls import path, include

from events import views


event_urlpatterns = [
    path('alarm/off', views.alarm_off),
    path('alarm/on/<str:date>', views.alarm_on),
]

urlpatterns = [
    path('events/', include(event_urlpatterns)),
]
