from django.contrib import admin

from auction.models import Auction, Dutch, English, Lot


class LotInLine(admin.StackedInline):
    model = Lot


class AuctionAdmin(admin.ModelAdmin):
    inlines = (LotInLine,)


admin.site.register(Lot)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Dutch)
admin.site.register(English)
