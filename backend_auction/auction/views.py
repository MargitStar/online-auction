from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from auction.models import Lot
from auction.serializers import LotSerializer


class LotViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)

    queryset = Lot.objects.all()
    serializer_class = LotSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['auction__current_price', 'auction__opening_date', 'auction__closing_date']
    filterset_fields = ('auction__status', 'auction__content_type__model')
