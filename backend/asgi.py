"""
Declares the ASGI application. Important that 'http' traffic gets handled by
the Django ASGI application as well, do NOT leave blank.
"""


from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from backend.webapp.urls import websocket_urlpatterns


application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
