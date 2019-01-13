from django.urls import path

from .views import index

from api import urls as api_urls


urlpatterns = [
    path("", index),
]
