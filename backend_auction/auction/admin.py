from django.contrib import admin

from .models import Auction, Dutch, English, Lot

admin.site.register(Lot)
admin.site.register(Auction)
admin.site.register(Dutch)
admin.site.register(English)