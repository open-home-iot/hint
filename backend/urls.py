from django.urls import path, include

from django.contrib import admin

from backend.webapp import urls as app_urls
from backend.api import urls as api_urls

from backend.webapp.urls import websocket_urlpatterns as app_ws_urlpatterns


urlpatterns = [
    path("api/", include(api_urls)),
    path("admin/", admin.site.urls),

    # Empty path will forward to front end Angular application.
    path("", include(app_urls)),
    # Catch all is forwarded to the Angular front end application, event 404's
    # are handled by the Angular application.
    path("<path:url>", include(app_urls)),
]

# Websocket URLs are routed to through the root routing.py
websocket_urlpatterns = app_ws_urlpatterns
