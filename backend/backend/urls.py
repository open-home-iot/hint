from django.urls import path, re_path, include
from django.conf.urls import url
from django.contrib import admin

from app import urls as app_urls
from api import urls as api_urls


urlpatterns = [
    path("app", include(app_urls)),
    path("api/", include(api_urls)),
    path("admin", admin.site.urls),
]

# TODO fill in
websocket_urlpatterns = [
    # url(regex, consumer)
    # url(regex, consumer)
]
