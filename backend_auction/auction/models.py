import decimal

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from item.models import Item

User = get_user_model()


class Auction(models.Model):
    class Status(models.IntegerChoices):
        PENDING = 1
        IN_PROGRESS = 2
        CLOSED = 3

    current_price = models.DecimalField(
        'current price, $',
        max_digits=10,
        decimal_places=2,
    )

    opening_price = models.DecimalField(
        'opening price, $',
        max_digits=10,
        decimal_places=2,
    )

    opening_date = models.DateTimeField(
        'opening date',
    )

    closing_date = models.DateTimeField(
        'closing date',
    )

    status = models.IntegerField(choices=Status.choices)

    object_id = models.IntegerField()

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )

    auction_type = GenericForeignKey('content_type', 'object_id')

    @property
    def opening_task_id(self):
        return f'lot-#{self.pk}-open-date'

    @property
    def closing_task_id(self):
        return f'lot-#{self.pk}-close-date'

    @property
    def updating_price_task_id(self):
        return f'lot-#{self.pk}-update-price'


class English(models.Model):
    buy_it_now = models.DecimalField(
        'buy it now price, $',
        max_digits=10,
        decimal_places=2,
    )

    reverse_price = models.DecimalField(
        'reverse price, $',
        max_digits=10,
        decimal_places=2,
    )

    auction = GenericRelation(Auction)


class Dutch(models.Model):
    end_price = models.DecimalField(
        'end price, $',
        max_digits=10,
        decimal_places=2,
    )

    frequency = models.DurationField(
    )

    @staticmethod
    def delta_price(auction):
        change_times = (auction.closing_date - auction.opening_date) // auction.auction_type.frequency
        delta_price = (auction.opening_price - auction.auction_type.end_price) / change_times
        return decimal.Decimal(delta_price)

    auction = GenericRelation(Auction)


class Lot(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    auction = models.OneToOneField(
        Auction,
        on_delete=models.CASCADE,

    )


class Offer(models.Model):
    lot = models.ForeignKey(
        Lot,
        on_delete=models.CASCADE,
        related_name='lot',
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
    )

    price = models.DecimalField(
        'price, $',
        max_digits=10,
        decimal_places=2,
    )

    timestamp = models.DateField(
        'timestamp',
        auto_now=True
    )
