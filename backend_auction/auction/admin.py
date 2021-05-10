import decimal

from django.contrib import admin

from auction.models import Auction, Dutch, English, Lot, Offer
from auction.tasks import close_auction, start_auction, update_price


class LotInLine(admin.StackedInline):
    model = Lot


class AuctionAdmin(admin.ModelAdmin):
    inlines = (LotInLine,)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        start_auction.apply_async((obj.pk,), eta=obj.opening_date, task_id=obj.opening_task_id)
        close_auction.apply_async((obj.pk,), eta=obj.closing_date, task_id=obj.closing_task_id)
        if obj.content_type.model == 'dutch':
            update_price.apply_async((obj.pk, 2), eta=obj.opening_date + obj.auction_type.frequency,
                                     task_id=obj.updating_price_task_id)


admin.site.register(Lot)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Dutch)
admin.site.register(English)
admin.site.register(Offer)
