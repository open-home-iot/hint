from django.urls import path, include

from api import urls as api_urls


urlpatterns = [
    path("", include(api_urls)),
]
