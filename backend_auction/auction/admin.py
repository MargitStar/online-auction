from django.contrib import admin

from auction.models import Auction, Dutch, English, Lot, Offer
from auction.tasks import close_auction, start_auction


class LotInLine(admin.StackedInline):
    model = Lot


class AuctionAdmin(admin.ModelAdmin):
    inlines = (LotInLine,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        start_auction.apply_async((obj.pk,), eta=obj.opening_date)
        close_auction.apply_async((obj.pk,), eta=obj.closing_date)


admin.site.register(Lot)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Dutch)
admin.site.register(English)
admin.site.register(Offer)
