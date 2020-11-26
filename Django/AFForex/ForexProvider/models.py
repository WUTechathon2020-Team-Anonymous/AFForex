from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.

class Currency_Chart(models.Model):
	name = models.CharField(max_length=100,unique=True, null=False, primary_key=True, default='chart')
	buy_cash = models.FloatField(default=1)
	buy_card = models.FloatField(default=1)
	sell_cash = models.FloatField(default=1)
	sell_card = models.FloatField(default=1)

	def __str__(self):
		return self.name

	# def save(self, *args, **kwargs):
	# 	is_new = not self.pk
	# 	super().save(*args, **kwargs)
	# 	if is_new:
	# 		ForexProvider.objects.create(usd=self)

	# @classmethod
	# def create(cls, name):
	# 	currency = cls(name=name)
	# 	return currency


class Currencies_List(models.Model):
	inr = models.FloatField(default=-1.0)
	usd = models.FloatField(default=-1.0)
	eur = models.FloatField(default=-1.0)
	gbp = models.FloatField(default=-1.0)
	aud = models.FloatField(default=-1.0)

	def __str__(self):
		return f'{self.id}'


class ForexProvider(models.Model):

	name = models.CharField(max_length=100, null=False, default='ForexProvider')
	site = models.URLField()
	inr = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='inr')
	usd = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='usd')
	eur = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='eur')
	gbp = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='gbp')
	aud = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='aud')
	lastupdated = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name



class Daily_Currencies_Value(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='daily_value')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)


class Buy_Cash_Low(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='buy_cash_low')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)

class Buy_Cash_High(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='buy_cash_high')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)

class Buy_Card_Low(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='buy_card_low')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)

class Buy_Card_High(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='buy_card_high')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)
		
class Sell_Cash_Low(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='sell_cash_low')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)

class Sell_Cash_High(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='sell_cash_high')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)

class Sell_Card_Low(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='sell_card_low')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)

class Sell_Card_High(models.Model):
	currencies = models.OneToOneField('Currencies_List', on_delete=models.PROTECT, null=True, blank=True, related_name='sell_card_high')
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)