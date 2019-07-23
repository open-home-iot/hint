from django.urls import path, include
from django.contrib import admin

from app import urls as app_urls
from api import urls as api_urls
from app.urls import websocket_urlpatterns as app_ws_urlpatterns


urlpatterns = [
    path("app", include(app_urls)),
    path("app/", include(app_urls)),
    path("api/", include(api_urls)),
    path("admin", admin.site.urls),
]

# TODO fill in
# Websocket URLs are routed to through the root routing.py
websocket_urlpatterns = app_ws_urlpatterns
