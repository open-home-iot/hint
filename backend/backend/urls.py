from django.urls import path, re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from app import urls as app_urls
from api import urls as api_urls


urlpatterns = [
    path("app", include(app_urls)),
    path("api/", include(api_urls)),
    path("admin", admin.site.urls),
]

# TODO fill in
# Websocket URLs are routed to through the root routing.py
websocket_urlpatterns = [
    # re_path(regex, consumer, name=)
    # re_path(regex, consumer, name=)
]
