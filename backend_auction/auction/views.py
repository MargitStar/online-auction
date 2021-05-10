from datetime import date

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auction.models import Auction, Lot, Offer
from auction.serializers import LotSerializer, OfferSerializer
from auction.validation import (validate_auction_buy_it_now_price,
                                validate_auction_price,
                                validate_auction_status)
from backend_auction.celery import app


@transaction.atomic
def create_offer(user, lot, serializer):
    Offer.objects.create(user=user, lot=lot, price=serializer.validated_data['price'])
    lot.auction.current_price = serializer.validated_data['price']
    lot.auction.save()


@transaction.atomic
def create_offer_buy_it_now(user, lot):
    Offer.objects.create(user=user, lot=lot, price=lot.auction.auction_type.buy_it_now)
    lot.auction.current_price = lot.auction.auction_type.buy_it_now
    lot.auction.status = Auction.Status.CLOSED
    app.control.revoke(lot.auction.closing_task_id)
    lot.auction.save()


@transaction.atomic
def buy_it_now_dutch(user, lot):
    Offer.objects.create(user=user, lot=lot, price=lot.auction.current_price)
    lot.auction.status = Auction.Status.CLOSED
    app.control.revoke(lot.auction.updating_price_task_id)
    app.control.revoke(lot.auction.closing_task_id)
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

    @action(detail=True, methods=['post'])
    def buy_it_now(self, request, pk=None):
        user = request.user
        lot = Lot.objects.get(pk=pk)
        if lot.auction.content_type.model == 'dutch':
            return Response("You can't buy dutch auction now!")
        if validate_auction_status(lot) and validate_auction_buy_it_now_price(lot):
            create_offer_buy_it_now(user, lot)
            return Response('You have just bought this auction!', status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def buy_it_now_dutch(self, request, pk=None):
        user = request.user
        lot = Lot.objects.get(pk=pk)
        if lot.auction.content_type.model == 'english':
            return Response("You can't buy english auction now!")
        if validate_auction_status(lot):
            buy_it_now_dutch(user, lot)
            return Response('You have just bought thia auction')