from django.apps import AppConfig


class AuctionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auction'

    def ready(self):
        from .signals import update_lot
        from django.db.models.signals import post_save
        from auction.models import Auction
        post_save.connect(update_lot, sender=Auction)
