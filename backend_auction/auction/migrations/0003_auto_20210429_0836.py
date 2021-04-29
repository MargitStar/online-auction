# Generated by Django 3.2 on 2021-04-29 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0002_dutch_english'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'In Progress'), (3, 'Closed')]),
        ),
        migrations.AlterField(
            model_name='english',
            name='buy_it_now',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='buy it now price, $'),
        ),
        migrations.AlterField(
            model_name='english',
            name='reverse_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='reverse price, $'),
        ),
    ]
