# Generated by Django 3.1.3 on 2020-11-23 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForexProvider', '0007_currency_chart_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='currency_chart',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_case'),
        ),
    ]
