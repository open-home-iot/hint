from django.urls import path

from backend.webapp.consumers import HumeConsumer


websocket_urlpatterns = [
    # as_asgi() is similar to how Django class based views
    # require the as_view() call. as_asgi() returns an
    # ASGI application to handle the incoming call.
    path("websocket", HumeConsumer.as_asgi()),
]
