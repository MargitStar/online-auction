from rest_framework import viewsets

from auction.serializers import LotSerializer
from auction.models import Lot


class LotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotSerializer

