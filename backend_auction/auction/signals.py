from auction.serializers import LotSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def update_lot(sender, instance, **kwargs):
    serializer = LotSerializer(instance.lot)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("lots", {
        "type": "lot_updated",
        "content": serializer.data,
    })
