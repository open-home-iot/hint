from django.urls import path

from backend.hume.views import (
    Humes,
    HumeFind,
    HumeConfirmPairing,
    HumeDiscoverDevices,
    HumeAttachDevice,
    BrokerCredentials
)
from backend.device.views import Devices, DeviceAction

urlpatterns = [
    # NOT AJAX
    path("", Humes.as_view()),
    path("broker-credentials", BrokerCredentials.as_view()),
    path("<str:hume_uuid>/devices", Devices.as_view()),

    # AJAX
    path("<str:hume_uuid>", HumeFind.as_view()),
    path("<str:hume_uuid>/confirm-pairing", HumeConfirmPairing.as_view()),
    path("<str:hume_uuid>/devices/discover", HumeDiscoverDevices.as_view()),
    path("<str:hume_uuid>/devices/<str:address>/attach",
         HumeAttachDevice.as_view()),
    path("<str:hume_uuid>/devices/<str:device_uuid>/action",
         DeviceAction.as_view())
]
