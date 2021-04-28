from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from item.models import Item


class Auction(models.Model):
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

    opening_date = models.DateField(
        'opening date',
    )

    closing_date = models.DateField(
        'closing date',
    )

    STATUS = (('PENDING', 'PENDING'), ('IN_PROGRESS', 'IN_PROGRESS'), ('CLOSED', 'CLOSED'))

    status = models.CharField(
        'status',
        max_length=15,
        choices=STATUS,
    )

    object_id = models.IntegerField()
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )

    auction_type = GenericForeignKey('content_type', 'object_id')


class English(models.Model):
    buy_it_now = models.DecimalField(
        'opening price, $',
        max_digits=10,
        decimal_places=2,
    )

    reverse_price = models.DecimalField(
        'opening price, $',
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

    frequency = models.DateTimeField(
        'frequency',
    )

    auction = GenericRelation(Auction)


class Lot(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    auction = models.OneToOneField(
        Auction,
        on_delete= models.CASCADE,

    )
