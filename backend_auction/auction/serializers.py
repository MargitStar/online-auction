from auction.models import Auction, Dutch, English, Lot, Offer
from item.serializers import ItemSerializer
from rest_framework import serializers


class AuctionObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Dutch):
            serializer = DutchSerializer(value)
            return serializer.data
        elif isinstance(value, English):
            serializer = EnglishSerializer(value)
            return serializer.data


class AuctionSerializer(serializers.ModelSerializer):
    auction_type = AuctionObjectRelatedField(read_only=True)

    class Meta:
        model = Auction
        exclude = ('object_id', 'content_type')


class EnglishSerializer(serializers.HyperlinkedModelSerializer):
    lot_type = serializers.ReadOnlyField(default='english')

    class Meta:
        model = English
        fields = ('lot_type', 'buy_it_now', 'reverse_price')


class DutchSerializer(serializers.HyperlinkedModelSerializer):
    lot_type = serializers.ReadOnlyField(default='dutch')

    class Meta:
        model = Dutch
        fields = ('lot_type', 'end_price', 'frequency')


class LotSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    auction = AuctionSerializer()

    class Meta:
        model = Lot
        fields = ('pk', 'item', 'auction')


class OfferSerializer(serializers.Serializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )


class OfferViewSerializer(serializers.ModelSerializer):
    lot = LotSerializer()

    class Meta:
        model = Offer
        fields = ('lot', 'user', 'price')
