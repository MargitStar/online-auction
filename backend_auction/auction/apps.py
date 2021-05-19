from django.apps import AppConfig


class AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auction'

    def ready(self):
        from auction.signals import update_lot, real_time_offer
        from django.db.models.signals import post_save
        from auction.models import Auction, Offer
        post_save.connect(update_lot, sender=Auction)
        post_save.connect(real_time_offer, sender=Offer)
