from django.urls import path, include

from .request_handling import handle_incoming_request


hume_patterns = [
    path("attach", handle_incoming_request,
         {'path': ('hume', 'attach',)}),
    path("authentication", handle_incoming_request,
         {'path': ('hume', 'authentication',)}),
    path("tokenupdate", handle_incoming_request,
         {'path': ('hume', 'token_update',)}),
]

device_patterns = [
    path("event", handle_incoming_request,
         {'path': ('device', 'event',)}),
]

urlpatterns = [
    path("hume/", include(hume_patterns)),
    path("device/", include(device_patterns)),

    # Generic for both devices and HUMEs
    path("heartbeat", handle_incoming_request,
         {'path': ('heartbeat', '',)}),
]
