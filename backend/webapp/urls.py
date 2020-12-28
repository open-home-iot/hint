from django.urls import path

from backend.webapp.views import AppView
from backend.webapp.consumers import HomeConsumer


urlpatterns = [
    path("", AppView.as_view())
]

websocket_urlpatterns = [
    # as_asgi() is similar to how Django class based views
    # require the as_view() call. as_asgi() returns an
    # ASGI application to handle the incoming call.
    path("", HomeConsumer.as_asgi()),
]
