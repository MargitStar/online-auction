from rest_framework import serializers

from auction.models import Auction, Dutch, English, Lot
from item.serializers import ItemSerializer


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
    class Meta:
        model = English
        fields = ('buy_it_now', 'reverse_price')


class DutchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dutch
        fields = ('end_price', 'frequency')


class LotSerializer(serializers.ModelSerializer):
    item = ItemSerializer(required=True)
    auction = AuctionSerializer(required=True)

    class Meta:
        model = Lot
        fields = ('item', 'auction')


class OfferSerializer(serializers.Serializer):
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
