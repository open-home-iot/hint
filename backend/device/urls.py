from django.urls import path

from backend.device.views import ChangeDeviceRoom


urlpatterns = [
    path("<str:device_uuid>/change-room", ChangeDeviceRoom.as_view())
]
