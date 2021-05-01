from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from auction.serializers import LotSerializer
from auction.models import Lot


class LotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['auction__current_price', 'auction__opening_date', 'auction__closing_date']
    filterset_fields = ('auction__status', 'auction__content_type__model')
