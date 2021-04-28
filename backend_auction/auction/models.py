from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from item.models import Item


class Lot(models.Model):
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
        primary_key=True,
    )


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

    auction_type_object_id = models.IntegerField()
    auction_type_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )

    auction_type = GenericForeignKey(
        'auction_type_content_type',
        'auction_type_object_id',
    )
