from rest_framework import routers

from auction.views import LotViewSet, OfferViewSet

router = routers.SimpleRouter()
router.register(r'lot', LotViewSet)
router.register(r'offer', OfferViewSet)

urlpatterns = router.urls

