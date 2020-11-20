from django.db import models
from django.utils import timezone

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



		