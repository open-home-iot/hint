from django.urls import path, include

from .views import info, heartbeat
from backend.hume.views import attach, authentication, token_update
from backend.events.views import event
from backend.user.views import login_user, logout_user


hume_patterns = [
    path("attach", attach),
    path("authentication", authentication),
    path("tokenupdate", token_update),
]

device_patterns = [
    path("event", event),
]

user_patterns = [
    path("login", login_user),
    path("logout", logout_user),
]

urlpatterns = [
    path("hume/", include(hume_patterns)),
    path("device/", include(device_patterns)),
    path("user/", include(user_patterns)),

    # Generic for both devices and HUMEs
    path("heartbeat", heartbeat),

    # API info
    path("info", info),
]
