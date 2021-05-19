import json

from channels.generic.websocket import AsyncWebsocketConsumer


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


class OfferConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "offers"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name,
        )
        await self.accept()

    async def offer_real_time(self, event):
        await self.send(text_data=json.dumps(event['text']))
