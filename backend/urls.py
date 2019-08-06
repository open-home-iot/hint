from django.urls import path, include

from backend.app import urls as app_urls
from backend.api_external import urls as api_ext_urls
from backend.api_internal import urls as api_int_urls
from backend.app.urls import websocket_urlpatterns as app_ws_urlpatterns


urlpatterns = [
    path("api/ext/", include(api_ext_urls)),

    # Empty path will forward to front end Angular application.
    path("", include(app_urls)),
    # Catch all is forwarded to the Angular front end application, event 404's
    # are handled by the Angular application.
    path("<path:url>", include(app_urls)),
]

# TODO fill in
# Websocket URLs are routed to through the root routing.py
websocket_urlpatterns = app_ws_urlpatterns
