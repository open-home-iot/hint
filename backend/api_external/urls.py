from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie

from .views import info, heartbeat
from backend.hume.views import attach, authentication, token_update
from backend.events.views import event


hume_patterns = [
    path("attach", attach),
    path("authentication", authentication),
    path("tokenupdate", token_update),
]

device_patterns = [
    path("event", event),
]

urlpatterns = [
    path("hume/", include(hume_patterns)),
    path("device/", include(device_patterns)),

    # Generic for both devices and HUMEs
    path("heartbeat", heartbeat),

    # API info
    path("info", ensure_csrf_cookie(info)),
]
