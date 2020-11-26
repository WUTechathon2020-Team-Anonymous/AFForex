import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currencies_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usd', models.FloatField(default=-1.0)),
                ('eur', models.FloatField(default=-1.0)),
                ('gbp', models.FloatField(default=-1.0)),
                ('aud', models.FloatField(default=-1.0)),
            ],
        ),
        migrations.CreateModel(
            name='Currency_Chart',
            fields=[
                ('name', models.CharField(default='chart', max_length=100, primary_key=True, serialize=False, unique=True)),
                ('buy_cash', models.FloatField(default=1)),
                ('buy_card', models.FloatField(default=1)),
                ('sell_cash', models.FloatField(default=1)),
                ('sell_card', models.FloatField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Sell_Cash_Low',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sell_cash_low', to='ForexProvider.currencies_list')),
            ],
        ),
        migrations.CreateModel(
            name='Sell_Cash_High',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sell_cash_high', to='ForexProvider.currencies_list')),
            ],
        ),
        migrations.CreateModel(
            name='Sell_Card_Low',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sell_card_low', to='ForexProvider.currencies_list')),
            ],
        ),
        migrations.CreateModel(
            name='Sell_Card_High',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sell_card_high', to='ForexProvider.currencies_list')),
            ],
        ),
        migrations.CreateModel(
            name='ForexProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='ForexProvider', max_length=100)),
                ('site', models.URLField()),
                ('aud', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='aud', to='ForexProvider.currency_chart')),
                ('eur', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='eur', to='ForexProvider.currency_chart')),
                ('gbp', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='gbp', to='ForexProvider.currency_chart')),
                ('usd', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='usd', to='ForexProvider.currency_chart')),
                ('lastupdated', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Buy_Cash_Low',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='buy_cash_low', to='ForexProvider.currencies_list')),
            ],
        ),
        migrations.CreateModel(
            name='Buy_Cash_High',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='buy_cash_high', to='ForexProvider.currencies_list')),
            ],
        ),
        migrations.CreateModel(
            name='Buy_Card_Low',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='buy_card_low', to='ForexProvider.currencies_list')),
            ],
        ),
        migrations.CreateModel(
            name='Buy_Card_High',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('currencies', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='buy_card_high', to='ForexProvider.currencies_list')),
            ],
        ),
    ]
