from django.urls import path, re_path, include

from app import urls as app_urls
from api import urls as api_urls


urlpatterns = [
    path("app", include(app_urls)),
    path("api/", include(api_urls)),
]
