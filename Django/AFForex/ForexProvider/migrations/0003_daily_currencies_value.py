# Generated by Django 3.1.3 on 2020-11-26 11:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ForexProvider', '0002_auto_20201126_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily_Currencies_Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='daily_value', to='ForexProvider.currencies_list')),
            ],
        ),
    ]
