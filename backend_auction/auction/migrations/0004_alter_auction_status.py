# Generated by Django 3.2 on 2021-04-29 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction', '0003_auto_20210429_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Progress'), (3, 'Closed')]),
        ),
    ]