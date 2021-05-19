from django.urls import path

from channels.routing import URLRouter

from auction.consumers import LotConsumer


websocket_urlpatterns = [
    path(
        "ws/notifications/",
        LotConsumer.as_asgi(),
        name="ws_notifications",
    ),
]
