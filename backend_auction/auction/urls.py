from rest_framework import routers

from auction.views import LotViewSet

router = routers.SimpleRouter()
router.register(r'', LotViewSet)

urlpatterns = router.urls
