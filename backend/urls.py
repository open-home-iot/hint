from django.urls import path, include
from django.contrib import admin

from backend.app import urls as app_urls
from backend.api import urls as api_urls
from backend.app.urls import websocket_urlpatterns as app_ws_urlpatterns


urlpatterns = [
    path("", include(app_urls)),
    path("app/", include(app_urls)),
    path("api/", include(api_urls)),
    path("admin", admin.site.urls),
]

# TODO fill in
# Websocket URLs are routed to through the root routing.py
websocket_urlpatterns = app_ws_urlpatterns
