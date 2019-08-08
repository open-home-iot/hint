from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from backend.urls import websocket_urlpatterns


application = ProtocolTypeRouter({
    # HTTP is handled by Django by default.
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
