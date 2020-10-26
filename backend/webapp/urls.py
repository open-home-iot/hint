from django.urls import path

from .views import AppView
from .consumers import HumeConsumer


urlpatterns = [
    path("", AppView.as_view(), name='index')
]

websocket_urlpatterns = [
    path("ws/test/<int:some_id>", HumeConsumer),
]
