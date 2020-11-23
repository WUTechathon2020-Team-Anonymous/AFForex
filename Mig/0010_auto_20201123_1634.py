# Generated by Django 3.1.3 on 2020-11-23 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForexProvider', '0009_auto_20201123_1620'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='forexprovider',
            constraint=models.UniqueConstraint(fields=('usd_id', 'eur_id', 'gbp_id', 'aud_id'), name='unique_currency'),
        ),
    ]