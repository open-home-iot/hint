from django.urls import path

from .views import AppView
from .consumers import HumeConsumer


urlpatterns = [
    path("", AppView.as_view(), name='index')
]

websocket_urlpatterns = [
    # as_asgi() is similar to how Django class based views
    # require the as_view() call. as_asgi() returns an
    # ASGI application to handle the incoming call.
    path("ws/test/<int:hume_id>", HumeConsumer.as_asgi()),
]
