# Generated by Django 3.1.3 on 2020-11-23 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ForexProvider', '0003_buy_cash_high_buy_cash_low'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency_Chart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_cash', models.FloatField()),
                ('buy_card', models.FloatField()),
                ('sell_cash', models.FloatField()),
                ('sell_card', models.FloatField()),
            ],
        ),
    ]