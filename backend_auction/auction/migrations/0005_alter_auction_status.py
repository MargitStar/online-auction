# Generated by Django 3.2 on 2021-04-29 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0004_alter_auction_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'In Progress'), (3, 'Closed')]),
        ),
    ]
