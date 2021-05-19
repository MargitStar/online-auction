import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class LotConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "lots"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def lot_updated(self, event):
        await self.send(text_data=json.dumps(event['content']))
