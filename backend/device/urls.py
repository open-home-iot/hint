from django.urls import path

from backend.device.views import ChangeDeviceRoom, Devices


urlpatterns = [
    path("", Devices.as_view()),
    path("<str:device_uuid>/change-room", ChangeDeviceRoom.as_view())
]
