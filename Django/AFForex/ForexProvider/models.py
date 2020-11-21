from django.db import models
from django.utils import timezone
from datetime import date

# Create your models here.
class ForexProvider(models.Model):
	name = models.CharField(max_length=100, null=False, default='ForexProvider')
	site = models.URLField()
	usd = models.FloatField()
	eur = models.FloatField()
	gbp = models.FloatField()
	aud = models.FloatField()
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
