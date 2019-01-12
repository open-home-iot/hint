from django.urls import path, include

from hume import urls as hume_urls
from device import urls as device_urls


urlpatterns = [
    path("hume/", include(hume_urls)),
]
