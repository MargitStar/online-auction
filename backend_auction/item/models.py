from django.db import models


class Item(models.Model):
    photo = models.ImageField(
        'Photo',
    )

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        max_length=1000,
    )
