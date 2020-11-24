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


class ForexProvider(models.Model):

	name = models.CharField(max_length=100, null=False, default='ForexProvider')
	site = models.URLField()
	usd = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='usd')
	eur = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='eur')
	gbp = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='gbp')
	aud = models.OneToOneField('Currency_Chart', on_delete=models.PROTECT, null=True, blank=True, related_name='aud')
	lastupdated = models.DateTimeField(default=timezone.now)


	def __str__(self):
		return self.name

class Buy_Cash_High(models.Model):
	usd = models.FloatField()
	eur = models.FloatField()
	gbp = models.FloatField()
	aud = models.FloatField()
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)

class Buy_Cash_Low(models.Model):
	usd = models.FloatField()
	eur = models.FloatField()
	gbp = models.FloatField()
	aud = models.FloatField()
	date = models.DateField(default=date.today)

	def __str__(self):
		return str(self.date)

		