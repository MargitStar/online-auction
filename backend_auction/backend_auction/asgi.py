"""
ASGI config for backend_auction project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_auction.settings')

asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from auction.routers import websocket_urlpatterns
from auction.ws_auth import TokenAuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket": TokenAuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns,
        )
    ),
})
