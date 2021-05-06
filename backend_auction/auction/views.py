from datetime import date

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auction.models import Auction, Lot, Offer
from auction.serializers import LotSerializer, OfferSerializer


def validate_auction_price(lot, serializer):
    if serializer.validated_data['price'] <= lot.auction.current_price:
        raise ValidationError("Price is less than it should be")
    return True


def validate_auction_status(lot):
    if lot.auction.status == Auction.Status.PENDING:
        raise ValidationError('Auction has not opened yet!')
    elif lot.auction.status == Auction.Status.CLOSED:
        raise ValidationError('Auction has already closed!')
    return True


@transaction.atomic
def create_offer(user, lot, serializer):
    Offer.objects.create(user=user, lot=lot, price=serializer.validated_data['price'])
    lot.auction.current_price = serializer.validated_data['price']
    lot.auction.save()


class LotViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['auction__current_price', 'auction__opening_date', 'auction__closing_date']
    filterset_fields = ('auction__status', 'auction__content_type__model')

    @action(detail=True, methods=['post'])
    def make_offer(self, request, pk=None):
        user = request.user
        serializer = OfferSerializer(data=request.data)
        lot = Lot.objects.get(pk=pk)
        if lot.auction.content_type.model == 'dutch':
            return Response("You can't make offer on dutch auction!")
        if serializer.is_valid():
            if validate_auction_price(lot, serializer) and validate_auction_status(lot):
                create_offer(user, lot, serializer)
                return Response('You have just made an offer', status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
