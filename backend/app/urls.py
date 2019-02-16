from django.urls import path, re_path

from .views import AppView
from .consumers import HumeConsumer


urlpatterns = [
    path("", AppView.as_view(), name='index'),
]

websocket_urlpatterns = [
    re_path(r'^ws/hume/(?P<hume_id>\d+)$', HumeConsumer),
]
